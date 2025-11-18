import React, {useState} from 'react'

const fieldStyle = {display:'flex', flexDirection:'column', marginBottom:12}
const labelStyle = {fontSize:13, color:'#344767', marginBottom:6}
const inputStyle = {padding:10, borderRadius:8, border:'1px solid #e6e9ef'}

const API_URL = 'http://10.248.253.17:8000'

export default function Form(){
  const [data, setData] = useState({attendance:80, study_hours:3, internal_marks:70, assignments_submitted:6, activities_participated:1})
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const onChange = (k, v) => setData({...data, [k]: v})

  const submit = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const json = await response.json()
      setResult(json)
    } catch (e) {
      setError(`Network Error: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:12}}>
        <div style={fieldStyle}>
          <label style={labelStyle}>Attendance (%)</label>
          <input style={inputStyle} type="number" value={data.attendance} onChange={e=>onChange('attendance', parseFloat(e.target.value))} />
        </div>
        <div style={fieldStyle}>
          <label style={labelStyle}>Study Hours (per day)</label>
          <input style={inputStyle} type="number" value={data.study_hours} onChange={e=>onChange('study_hours', parseFloat(e.target.value))} />
        </div>
        <div style={fieldStyle}>
          <label style={labelStyle}>Internal Marks</label>
          <input style={inputStyle} type="number" value={data.internal_marks} onChange={e=>onChange('internal_marks', parseFloat(e.target.value))} />
        </div>
        <div style={fieldStyle}>
          <label style={labelStyle}>Assignments Submitted</label>
          <input style={inputStyle} type="number" value={data.assignments_submitted} onChange={e=>onChange('assignments_submitted', parseInt(e.target.value))} />
        </div>
        <div style={{gridColumn:'1/3', ...fieldStyle}}>
          <label style={labelStyle}>Activities Participated</label>
          <input style={inputStyle} type="number" value={data.activities_participated} onChange={e=>onChange('activities_participated', parseInt(e.target.value))} />
        </div>
      </div>

      <div style={{display:'flex', gap:10, marginTop:16}}>
        <button onClick={submit} style={{padding:'10px 16px', borderRadius:8, border:'none', background:'#0b69ff', color:'#fff', cursor:'pointer'}}>Predict</button>
      </div>

      <div style={{marginTop:20}}>
        {loading && <div style={{color:'#2b6cb0', fontSize:14}}>Loading...</div>}
        {error && <div style={{color:'#e53e3e', fontSize:14}}>{error}</div>}
        {result && (
          <div style={{padding:14, borderRadius:8, background:'#f7fbff', marginTop:8}}>
            <div style={{fontSize:20, color:'#0b2545', fontWeight:'bold'}}>Result: {result.prediction}</div>
            <div style={{color:'#475569', marginTop:8}}>Confidence: {(result.confidence*100).toFixed(1)}%</div>
          </div>
        )}
      </div>
    </div>
  )
}
