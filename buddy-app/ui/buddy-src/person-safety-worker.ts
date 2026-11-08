import * as tf from '@tensorflow/tfjs-core';
import {loadGraphModel,type GraphModel} from '@tensorflow/tfjs-converter';
import '@tensorflow/tfjs-backend-cpu';
import type {BodyPose} from './person-safety.ts';
type PoseRequest = {type:'init';modelUrl:string}|{type:'frame';bitmap:ImageBitmap;time:number};
let model:GraphModel|null=null;
const scope=self as unknown as {onmessage:((event:MessageEvent<PoseRequest>)=>void)|null;postMessage:(data:unknown)=>void};
scope.onmessage=async({data})=>{
 try{
  if(data.type==='init'){if(!await tf.setBackend('cpu'))throw Error('CPU backend unavailable');await tf.ready();model=await loadGraphModel(data.modelUrl);scope.postMessage({type:'ready'});}
  if(data.type==='frame'){
   const began=performance.now();
   const bitmap=data.bitmap;let input:tf.Tensor|undefined,outputs:tf.Tensor[]=[];
   try{
    if(!model)throw Error('Model chưa sẵn sàng');
    const w=bitmap.width,h=bitmap.height,scale=256/Math.max(w,h),rw=Math.max(1,Math.round(w*scale)),rh=Math.max(1,Math.round(h*scale)),pw=Math.ceil(rw/32)*32,ph=Math.ceil(rh/32)*32;
    const canvas=new OffscreenCanvas(w,h);const ctx=canvas.getContext('2d');if(!ctx)throw Error('Canvas unavailable');ctx.drawImage(bitmap,0,0);
    const modelInput=tf.tidy(()=>tf.expandDims(tf.cast(tf.pad(tf.image.resizeBilinear(tf.browser.fromPixels(ctx.getImageData(0,0,w,h)),[rh,rw]),[[0,ph-rh],[0,pw-rw],[0,0]]),'int32'),0));input=modelInput;
    const output=await model.executeAsync(modelInput);outputs=Array.isArray(output)?output:[output];const tensor=outputs.find(t=>t.shape.at(-1)===56);if(!tensor)throw Error('Đầu ra MoveNet không hợp lệ');
    const values=await tensor.data(),poses:BodyPose[]=[];
    for(let offset=0;offset+55<values.length&&offset<6*56;offset+=56){
     const at=(index:number)=>Number(values[offset+index]);
     const score=at(55);
     if(!Number.isFinite(score)||score<.35)continue;
     const joints=Array.from({length:17},(_,i)=>({x:at(i*3+1)*pw/rw,y:at(i*3)*ph/rh,score:at(i*3+2)}));
     const x=at(52)*pw/rw,y=at(51)*ph/rh;
     poses.push({score,joints,box:{x,y,width:at(54)*pw/rw-x,height:at(53)*ph/rh-y}});
    }
    scope.postMessage({type:'result',time:data.time,poses,inferenceMs:Math.round(performance.now()-began)});
   }finally{bitmap.close();input?.dispose();outputs.forEach(t=>t.dispose());}
  }
 }catch{scope.postMessage({type:'error',message:'Không chạy được MoveNet trên máy này. Tắt/bật phân tích tư thế để thử lại.'});}
};
