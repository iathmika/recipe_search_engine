import React, {useState} from 'react'

function Advsearch() {
    const [state, setstate] = useState(false);
const show=()=>{
    setstate(true);
}
const hide=()=>{
    setstate(false);
}
  return (
    
    <div className='Advsearch'>
        <div className='Advsearch_options' onMouseEnter={show} onMouseLeave={hide} >
            Advanced Search
            {state?<ul className="Advsearch_dropoptions" onMouseEnter={show}>
                <li>Boolean</li>
                <li>BM25</li>
                <li>tf-idf</li>

            </ul>:null}
            

        </div>
    </div>
  )
}

export default Advsearch