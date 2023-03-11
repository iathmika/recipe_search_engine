import styled from "styled-components";
import { FaSearch } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import image from "../images/bg.jpeg";
import Button from "./Button"
import React from "react";
//import { MDBBtn } from 'mdb-react-ui-kit';
function Search() {
  const [input, setInput] = useState("");

  let navigate = useNavigate();
  const data = fetch(			
    `http://localhost:8000/index/`
);
  const submitHandler = (e) => {
    e.preventDefault();
    navigate(`/searched/${input}`);
    console.log(e);
  };

  /* return (
    <FormStyle onSubmit={submitHandler}>
      <div>
        <FaSearch />
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        
      
  
      </div>
      
      <Button text="Search" onClick={submitHandler} />  
    </FormStyle>

    
  );
*/
  return (
   
      <FormStyle onSubmit={submitHandler}>
     
    
        <FaSearch />
        <input
          type="text"
          placeholder="Search for your Recipe here!"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        /> 
  
    
         <Button text="Search" onClick={submitHandler} />
        
        
    </FormStyle> 
 

  )
}
//
const FormStyle = styled.form`
  position: relative;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  width: 100%;
  display: flex;
  
  justify-content: center;
  align-items: center;

  

  div {
    align-items: center;
    position: relative;
    width: 100%;
    display: block;
    justify-content: center;

  }

  input {
   
    border: none;
    background: linear-gradient(35deg, #494949, #313131);
    font-size: 2rem;
    font-family: "Ink Free", sans-serif;
    font-color: white;
    color: white;
    padding: 1rem 3rem;
    border-radius: 1rem;
    outline: none;
    height: 80%;
    width: 80%;
    opacity: 0.90;
    
  }

  svg {
    position: relative;
    top: 50%;
    left: 3% ;
    transform: translate(0%, 0%);
    color: white;
    
  }
`;

export default Search;
