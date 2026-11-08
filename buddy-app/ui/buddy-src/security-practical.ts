export type WatchRegion={x:number;y:number;width:number;height:number};
export const FULL_REGION:WatchRegion={x:0,y:0,width:1,height:1};
export function normalizeRegion(r:WatchRegion):WatchRegion{const clamp=(n:number,min:number,max:number)=>Number.isFinite(n)?Math.max(min,Math.min(max,n)):min;const x=clamp(r.x,0,.9),y=clamp(r.y,0,.9);return {x,y,width:clamp(r.width,.1,1-x),height:clamp(r.height,.1,1-y)};}
export function inWatchSchedule(enabled:boolean,start:string,end:string,date=new Date()){
 if(!enabled)return true;
 if(!/^([01]\d|2[0-3]):[0-5]\d$/.test(start)||!/^([01]\d|2[0-3]):[0-5]\d$/.test(end))return false;
 const minutes=(s:string)=>Number(s.slice(0,2))*60+Number(s.slice(3));const now=date.getHours()*60+date.getMinutes(),a=minutes(start),b=minutes(end);
 return a===b?true:a<b?now>=a&&now<b:now>=a||now<b;
}
export {inspectScam, type ScamSignal} from './scam-inspector.ts';
