import React from 'react';
import "../index.css"
import { useNavigate } from "react-router-dom";
function Button({FAQ, onClick }) {
    const navigate = useNavigate();

    function handleClick() {
      navigate("/faqs");}
    return ( <button className="button" onClick={handleClick}> FAQs
    </button>
    );
}


export default Button;

