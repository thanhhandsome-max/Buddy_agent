/** @jsxImportSource react */
import {useMemo} from 'react';
import {coderInlineDiff} from './coder-inline-diff.ts';

export function CoderInlineDiff({oldText,newText}:{oldText:string;newText:string}){
 const diff=useMemo(()=>coderInlineDiff(oldText,newText),[oldText,newText]);
 return <div className="coder-inline-diff" role="table" aria-label="So sánh mã nguồn trước và sau khi sửa">
  <div className="coder-inline-diff-legend"><span><i className="coder-inline-swatch removed"/> {diff.removed} dòng xóa</span><span><i className="coder-inline-swatch added"/> {diff.added} dòng thêm</span></div>
  {diff.sections.map((section,index)=>section.kind==='fold'?<div className="coder-diff-fold" role="row" key={'fold-'+index}><span aria-hidden="true">···</span><span>{section.count} dòng không đổi đã thu gọn</span></div>:<section className="coder-diff-hunk" aria-label={`Đoạn thay đổi ${index+1}`} key={'hunk-'+index}>
   {section.rows.map((row,rowIndex)=><div className={'coder-diff-row '+row.kind} role="row" key={`${index}-${rowIndex}`}>
    <span className="coder-diff-number old" aria-label={row.oldLine===null?'Dòng mới':'Dòng cũ '+row.oldLine}>{row.oldLine??''}</span><span className="coder-diff-number new" aria-label={row.newLine===null?'Dòng đã xóa':'Dòng mới '+row.newLine}>{row.newLine??''}</span><span className="coder-diff-marker" aria-hidden="true">{row.kind==='added'?'+':row.kind==='removed'?'−':' '}</span><code>{row.text||' '}</code>
   </div>)}
  </section>)}
  {!diff.sections.length&&<p className="coder-diff-identical">Nội dung không đổi.</p>}
 </div>;
}
