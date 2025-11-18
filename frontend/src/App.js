import React from 'react'
import Form from './components/Form'

const App = () => {
  return (
    <div style={{fontFamily:'Inter, Arial, sans-serif', display:'flex', minHeight:'100vh', alignItems:'center', justifyContent:'center', background:'#f3f6ff'}}>
      <div style={{width:760, background:'#fff', padding:28, borderRadius:12, boxShadow:'0 8px 24px rgba(20,36,60,0.08)'}}>
        <header style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:18}}>
          <h2 style={{margin:0, color:'#0b2545'}}>Student Performance Predictor</h2>
        </header>
        <Form />
      </div>
    </div>
  )
}

export default App
