/** Prototype temporal rules, not a trained fall classifier or medical assessment. */
export type Joint={x:number;y:number;score:number};
export type BodyPose={score:number;box:{x:number;y:number;width:number;height:number};joints:Joint[]};
export type PersonAlert={track:number;kind:'possible-fall'|'low-motion';message:string};
type Track={id:number;pose:BodyPose;last:number;uprightSince:number|null;uprightAt:number;uprightHip:number;horizontalSince:number|null;stillSince:number|null;stillAnchor:BodyPose|null;fallCandidate:boolean;fallSent:boolean;stillSent:boolean};
export function overlap(a:BodyPose['box'],b:BodyPose['box']){const area=Math.max(0,Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y));return area/(a.width*a.height+b.width*b.height-area||1);}
function geometry(p:BodyPose,aspect:number){
 const [leftShoulder,rightShoulder,leftHip,rightHip,leftAnkle,rightAnkle]=[5,6,11,12,15,16].map(i=>p.joints[i]);
 if(p.score<.35||!leftShoulder||!rightShoulder||!leftHip||!rightHip||!leftAnkle||!rightAnkle)return null;
 const joints=[leftShoulder,rightShoulder,leftHip,rightHip,leftAnkle,rightAnkle];
 if(joints.some(j=>!Number.isFinite(j.score)||j.score<.4||!Number.isFinite(j.x)||!Number.isFinite(j.y)||j.x<0||j.x>1||j.y<0||j.y>1))return null;
 const mid=(a:Joint,b:Joint)=>({x:(a.x+b.x)/2,y:(a.y+b.y)/2});
 const shoulder=mid(leftShoulder,rightShoulder),hip=mid(leftHip,rightHip),ankle=mid(leftAnkle,rightAnkle);
 const dx=Math.abs(hip.x-shoulder.x)*aspect,dy=Math.abs(hip.y-shoulder.y);
 return {hip:hip.y,upright:dy>dx*1.5&&ankle.y-shoulder.y>.18,horizontal:dx>dy*1.5&&p.box.width*aspect>p.box.height*1.1};
}
export class PersonSafetyTracker{
 private tracks:Track[]=[];private next=1;private last=-1;
 reset(){this.tracks=[];this.last=-1;}
 update(poses:BodyPose[],time:number,aspect=1,stillMs=30000){
  if(!Number.isFinite(time)||time<=this.last||!Number.isFinite(aspect)||aspect<=0)return {people:0,alerts:[] as PersonAlert[]};
  if(this.last>=0&&time-this.last>1500)this.tracks=[];
  this.last=time;this.tracks=this.tracks.filter(t=>time-t.last<=1500);const used=new Set<number>(),alerts:PersonAlert[]=[];
  const valid=poses.filter(p=>Number.isFinite(p.score)&&p.score>=.35&&p.box.width>.05&&p.box.height>.05&&[p.box.x,p.box.y,p.box.width,p.box.height].every(Number.isFinite)).slice(0,6);
  for(const pose of valid){
   const candidates=this.tracks.filter(t=>!used.has(t.id)).map(t=>({t,iou:overlap(t.pose.box,pose.box)})).filter(x=>x.iou>.15).sort((a,b)=>b.iou-a.iou);
   const [closest,next]=candidates;
   let t=closest&&next&&closest.iou-next.iou<.1?undefined:closest?.t;
   if(!t){t={id:this.next++,pose,last:time,uprightSince:null,uprightAt:-Infinity,uprightHip:0,horizontalSince:null,stillSince:null,stillAnchor:null,fallCandidate:false,fallSent:false,stillSent:false};this.tracks.push(t);}
   used.add(t.id);const g=geometry(pose,aspect);
   if(!g){t.uprightSince=null;t.uprightAt=-Infinity;t.horizontalSince=null;t.stillSince=null;t.fallCandidate=false;t.fallSent=false;t.stillSent=false;}
   else if(g.upright){t.uprightSince??=time;if(time-t.uprightSince>=1500){t.uprightAt=time;t.uprightHip=g.hip;}t.horizontalSince=null;t.stillSince=null;t.fallCandidate=false;t.fallSent=false;t.stillSent=false;}
   else if(g.horizontal){
    if(t.horizontalSince===null){t.horizontalSince=time;t.stillSince=time;t.stillAnchor=pose;t.fallCandidate=time-t.uprightAt<=2000&&g.hip-t.uprightHip>.1;}
    t.uprightSince=null;
    const anchor=t.stillAnchor??pose,indices=[5,6,11,12,15,16];
    const displacement=Math.max(...indices.map(i=>{
     const current=pose.joints[i],original=anchor.joints[i];
     return current&&original?Math.hypot((current.x-original.x)*aspect,current.y-original.y):Infinity;
    }));
    if(displacement>.025){t.stillSince=time;t.stillAnchor=pose;}
    if(t.fallCandidate&&!t.fallSent&&time-t.horizontalSince>=1200){t.fallSent=true;alerts.push({track:t.id,kind:'possible-fall',message:`Nghi chuyển nhanh từ đứng sang nằm ở dấu theo dõi #${t.id}. Cần xem ảnh và xác minh trực tiếp; chưa xác nhận ngã hay cấp cứu.`});}
    if(!t.stillSent&&t.stillSince!==null&&time-t.stillSince>=Math.max(10000,stillMs)){t.stillSent=true;alerts.push({track:t.id,kind:'low-motion',message:`Tư thế nằm ít chuyển động khoảng ${Math.round((time-t.stillSince)/1000)} giây ở dấu theo dõi #${t.id}. Có thể đang nghỉ; cần người nhận xác minh, không kết luận bất tỉnh.`});}
   }else{t.uprightSince=null;t.horizontalSince=null;t.stillSince=null;t.fallCandidate=false;}
   t.pose=pose;t.last=time;
  }
  // Missing/occluded people do not accrue inactivity time or carry standing history.
  this.tracks=this.tracks.filter(t=>used.has(t.id));
  return {people:valid.length,alerts};
 }
}
