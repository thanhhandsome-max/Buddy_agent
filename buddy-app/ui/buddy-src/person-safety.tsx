/** @jsxImportSource react */
import {useEffect,useRef,useState,type RefObject} from 'react';
import {PersonSafetyTracker,type BodyPose} from './person-safety.ts';
import {inWatchSchedule,type WatchRegion} from './security-practical.ts';
type Props={modelUrl:string;video:RefObject<HTMLVideoElement|null>;live:boolean;armed:boolean;region:WatchRegion;scheduled:boolean;from:string;to:string;evidence:boolean;onAlert:(message:string,image?:string)=>void};
export function PersonSafety(props:Props){
 const [enabled,setEnabled]=useState(false),[status,setStatus]=useState('Chưa bật phân tích tư thế'),[people,setPeople]=useState(0),[stillSeconds,setStillSeconds]=useState(30),[elapsed,setElapsed]=useState(0);
 const current=useRef({...props,stillSeconds});current.current={...props,stillSeconds};
 useEffect(()=>{
  if(!enabled||!props.live){setPeople(0);setElapsed(0);setStatus(enabled?'Bật camera để dùng model':'Chưa bật phân tích tư thế');return;}
  const worker=new Worker(new URL('./person-safety-worker.ts', import.meta.url), {type:'module'}),tracker=new PersonSafetyTracker(),canvas=document.createElement('canvas');const context=canvas.getContext('2d');
  let disposed=false,failed=false,ready=false,pending=false,sentAt=0,capturedAt=0,lastVideo=-1,config='',lastAlert=-Infinity,initial=performance.now(),frameImage:string|undefined,timer:ReturnType<typeof setInterval>|undefined;
  setStatus('Đang nạp MoveNet tại máy…');
  function fail(message:string){if(disposed||failed)return;failed=true;clearInterval(timer);setStatus(message);setPeople(0);tracker.reset();ready=false;pending=false;worker.terminate();}
  worker.onerror=()=>fail('Lỗi bộ phân tích. Tắt/bật phân tích tư thế để thử lại.');
  worker.onmessage=({data})=>{
   if(disposed)return;
   if(data.type==='ready'){ready=true;setStatus('Model sẵn sàng — bật trông khu vực để theo dõi');return;}
   if(data.type==='error'){fail(data.message);return;}
   if(data.type!=='result')return;pending=false;setElapsed(Math.round(performance.now()-sentAt));
   const p=current.current;
   if(data.time!==capturedAt||performance.now()-capturedAt>1500||!p.armed||!inWatchSchedule(p.scheduled,p.from,p.to)||config!==JSON.stringify([p.region,p.stillSeconds,p.scheduled,p.from,p.to])){tracker.reset();setPeople(0);setStatus('Chờ bật trông, đúng lịch hoặc khung hình mới');return;}
   const result=tracker.update(data.poses as BodyPose[],data.time,canvas.width/canvas.height,p.stillSeconds*1000);setPeople(result.people);setStatus(result.people?'Đang theo dõi tư thế trong vùng chọn':'Chưa thấy người đủ rõ trong vùng chọn');
   for(const alert of result.alerts)if(performance.now()-lastAlert>=15000){lastAlert=performance.now();p.onAlert(alert.message,p.evidence?frameImage:undefined);}
  };
  worker.postMessage({type:'init',modelUrl:props.modelUrl});
  timer=setInterval(async()=>{
   if(disposed)return;const p=current.current,video=p.video.current,now=performance.now();
   if(!ready){if(now-initial>45000)fail('Nạp model quá lâu. Tắt/bật phân tích tư thế để thử lại.');return;}
   if(pending){if(now-sentAt>8000)fail('Model phản hồi quá lâu. Đã dừng phân tích tư thế để giữ giao diện hoạt động.');return;}
   if(!p.armed||!inWatchSchedule(p.scheduled,p.from,p.to)||document.hidden){tracker.reset();setPeople(0);setStatus('Chờ bật trông hoặc khung giờ đã chọn');return;}
   if(!context||!video||video.readyState<2){tracker.reset();setPeople(0);setStatus('Đang chờ khung hình mới; chưa đánh giá tư thế');return;}
   if(lastVideo===video.currentTime){if(now-sentAt>1500){tracker.reset();setPeople(0);setStatus('Đang chờ khung hình mới; chưa đánh giá tư thế');}return;}
   const signature=JSON.stringify([p.region,p.stillSeconds,p.scheduled,p.from,p.to]);if(config!==signature){tracker.reset();config=signature;}
   lastVideo=video.currentTime;const r=p.region,w=video.videoWidth*r.width,h=video.videoHeight*r.height,scale=Math.min(1,480/Math.max(w,h));canvas.width=Math.max(32,Math.round(w*scale));canvas.height=Math.max(32,Math.round(h*scale));
   pending=true;sentAt=now;capturedAt=now;
   try{context.drawImage(video,video.videoWidth*r.x,video.videoHeight*r.y,w,h,0,0,canvas.width,canvas.height);frameImage=p.evidence?canvas.toDataURL('image/jpeg',.65):undefined;const bitmap=await createImageBitmap(canvas);if(disposed){bitmap.close();return;}worker.postMessage({type:'frame',bitmap,time:now},[bitmap]);}catch{pending=false;tracker.reset();setPeople(0);setStatus('Không đọc được khung hình để phân tích tư thế');}
  },500);
  return()=>{disposed=true;clearInterval(timer);worker.terminate();tracker.reset();};
 },[enabled,props.live,props.modelUrl]);
 return <section className="panel security-person-model"><div className="security-panel-title"><h2>Người & dấu hiệu cần kiểm tra</h2><span>MoveNet MultiPose · tối đa 6 tư thế · xử lý CPU tại máy</span></div><label className="security-check"><input type="checkbox" checked={enabled} onChange={e=>setEnabled(e.target.checked)}/> Bật phân tích tư thế thử nghiệm</label><p role="status">{status}</p><div className="security-metrics"><div><strong>{people}</strong><span>Tư thế đủ rõ ở khung gần nhất</span></div><div><strong>{elapsed} ms</strong><span>Thời gian xử lý lần gần nhất</span></div></div><label>Cảnh báo tư thế nằm ít chuyển động sau<select aria-label="Thời gian ít chuyển động" value={stillSeconds} onChange={e=>setStillSeconds(Number(e.target.value))}><option value={15}>15 giây</option><option value={30}>30 giây</option><option value={60}>60 giây</option></select></label><p className="security-caption">Phát hiện khớp cơ thể bằng model, rồi dùng quy tắc thời gian để báo nghi chuyển từ đứng sang nằm hoặc nằm ít chuyển động. Cần thấy rõ toàn thân; mất khớp, mất hình hoặc xử lý quá chậm sẽ xóa lịch sử. Số thứ tự theo dõi không phải danh tính.</p><p className="security-sample">Chưa được kiểm chứng trên video ngã thực tế. Không xác nhận cấp cứu, bất tỉnh hay đánh nhau; tập thể dục/nghỉ ngơi có thể gây báo nhầm. Luôn cần người nhận xác minh. Ảnh minh chứng dùng tùy chọn của phiên camera.</p></section>;
}
