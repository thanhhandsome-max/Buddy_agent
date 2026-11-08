/** Local, deterministic log triage. Findings are signals, not confirmed incidents. */
import {correlateSecurityEvents} from './security-correlation.ts';
export type SecuritySeverity = 'high' | 'medium' | 'info';
export type SecurityFinding = {id:string;severity:SecuritySeverity;title:string;line:number;evidence:string;recommendation:string;source:string};
export type SecurityReport = {lines:number;parsed:number;findings:SecurityFinding[];truncated:boolean};
export const MAX_LOG_BYTES = 1024 * 1024;
export const MAX_LOG_LINES = 5000;
const record = (value:unknown):Record<string,unknown> => value && typeof value==='object' && !Array.isArray(value) ? value as Record<string,unknown> : {};
const text = (value:unknown) => typeof value==='string' || typeof value==='number' ? String(value) : '';

export function analyzeSecurityLog(input:string):SecurityReport {
 if(new TextEncoder().encode(input).byteLength>MAX_LOG_BYTES)throw Error('Log vượt giới hạn 1 MB. Hãy chọn một đoạn nhỏ hơn.');
 const all=input.split(/\r?\n/), lines=all.slice(0,MAX_LOG_LINES), findings:SecurityFinding[]=[];
 let parsed=0,failedLogins=0,firstFailure=0;
 const add=(line:number,severity:SecuritySeverity,title:string,recommendation:string,source:string)=>{
  if(findings.length>=200)return;
  findings.push({id:`${line}-${findings.length}`,line,severity,title,recommendation,source,evidence:lines[line-1]?.slice(0,700)??''});
 };
 lines.forEach((raw,index)=>{
  if(!raw.trim())return;
  const line=index+1;
  let entry:Record<string,unknown>={};
  try{entry=record(JSON.parse(raw));if(Object.keys(entry).length)parsed++;}catch{/* Plain text remains eligible for explicit rules. */}
  const alert=record(entry.alert),win=record(record(entry.win).system),system=record(entry.System);
  const eventId=text(entry.EventID??entry.event_id??win.eventID??system.EventID);
  if(entry.event_type==='alert'){
   const severity=Number(alert.severity);
   add(line,severity===1?'high':severity===2?'medium':'info',`IDS: ${text(alert.signature).slice(0,180)||'Cảnh báo từ sensor'}`,'Đối chiếu IP, thời điểm và lưu lượng liên quan trước khi kết luận.','Suricata EVE');
  }
  if(eventId==='4625'||/\bfailed password for\b|\bauthentication failure\b|\blogon failure\b/i.test(raw)){
   failedLogins++;if(!firstFailure)firstFailure=line;
   add(line,'medium','Đăng nhập thất bại','Kiểm tra tài khoản, nguồn truy cập và khả năng nhập sai mật khẩu.','Luật đăng nhập');
  }
  if(eventId==='1102'||/\baudit log (?:was )?cleared\b|\bevent log (?:was )?cleared\b/i.test(raw))
   add(line,'high','Nhật ký kiểm toán bị xóa','Xác minh thao tác quản trị có chủ đích; đối chiếu log được lưu ở nơi khác.','Luật kiểm toán');
  if(eventId==='4720')add(line,'info','Tài khoản Windows mới được tạo','Đối chiếu người tạo và yêu cầu cấp tài khoản.','Windows Event');
  if(eventId==='4732')add(line,'medium','Thành viên được thêm vào nhóm cục bộ','Kiểm tra nhóm đích có quyền quản trị không và việc cấp quyền có hợp lệ không.','Windows Event');
  // Only explicit PowerShell switches; a textual hit does not prove execution or malware.
  if(/\b(?:powershell|pwsh)(?:\.exe)?\b[^\r\n]{0,500}\s-(?:enc|encodedcommand)\b/i.test(raw))
   add(line,'medium','Tham số PowerShell mã hóa xuất hiện trong log','Kiểm tra sự kiện thực thi và tiến trình cha. Chuỗi này cũng có thể nằm trong tài liệu hoặc tác vụ hợp lệ.','Luật dòng lệnh');
 });
 if(failedLogins>=3)add(firstFailure,'medium',`${failedLogins} dòng đăng nhập thất bại trong đoạn log`,'Chưa kết luận brute force: cần nhóm theo IP/tài khoản và cửa sổ thời gian.','Tổng hợp đoạn log');
 findings.push(...correlateSecurityEvents(lines).slice(0,Math.max(0,200-findings.length)));
 return {lines:lines.filter(l=>l.trim()).length,parsed,findings:findings.sort((a,b)=>({high:0,medium:1,info:2}[a.severity]-{high:0,medium:1,info:2}[b.severity])||a.line-b.line),truncated:all.length>MAX_LOG_LINES||findings.length>=200};
}

/** Fraction of sample pixels changing substantially; light/exposure also triggers this. */
export function frameChange(previous:Uint8ClampedArray,current:Uint8ClampedArray):number {
 if(!previous.length||previous.length!==current.length)return 0;
 let changed=0,pixels=0;
 for(let i=0;i+3<current.length;i+=4){
  pixels++;
  const delta=(Math.abs((current[i]??0)-(previous[i]??0))
    +Math.abs((current[i+1]??0)-(previous[i+1]??0))
    +Math.abs((current[i+2]??0)-(previous[i+2]??0)))/3;
  if(delta>30)changed++;
 }
 return pixels?changed/pixels:0;
}

export const SECURITY_SAMPLE_LOG = [
 JSON.stringify({timestamp:'2026-10-22T09:00:00Z',event_type:'alert',src_ip:'192.0.2.10',dest_ip:'198.51.100.20',alert:{severity:2,signature:'DEMO — kết nối cần kiểm tra'}}),
 JSON.stringify({TimeCreated:'2026-10-22T09:01:00Z',EventID:4625,AccountName:'demo-user'}),
 JSON.stringify({TimeCreated:'2026-10-22T09:02:00Z',EventID:1102,Message:'DEMO — audit log cleared'}),
 '2026-10-22T09:03:00Z demo-host sshd: Failed password for demo-user from 192.0.2.10 port 12345 ssh2',
 '2026-10-22T09:04:00Z demo-host sshd: Failed password for demo-user from 192.0.2.10 port 12346 ssh2',
].join('\n');
