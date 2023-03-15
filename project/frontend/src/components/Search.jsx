import styled from "styled-components";
import { FaSearch } from "react-icons/fa";
import { FaTimes } from "react-icons/fa";
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

  const handleClearBtn = () => {
    setInput('');
  }

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

     
    
        <div class="search-bar">
          <div class="search-box">
          <input
            type="text"
            placeholder="Search for your Recipe here!"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            autofocus required/> 
            <FaTimes // Cross Button 
            onClick={handleClearBtn}/>
          </div>
         
          <FaSearch  // Search Logo Button
          onClick={submitHandler} /> </div>
      
        
        
        
    </FormStyle> 
 

  )
}
// <Button text="Search" onClick={submitHandler} />
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

  
  .fa-times:hover {
    cursor: pointer;
  }
  div {
    align-items: center;
    position: relative;
    width: 100%;
    display: block;
    justify-content: center;
    border: 2px solid #ccc;

  }
 
  input {
   
    border: 0;
    position: relative;
    background: transprent;
    font-size: 2rem;
    font-family: "Ink Free", sans-serif;
    font-color: black;
    
    padding: 1rem 1rem;
    border-radius: 0rem;
    outline: none;
    height: 100%;
    width: 92%;
    opacity: 0.75;
    &::placeholder {
      color: var(--color);
      opacity: 0.75;
    }
   
    
  }
  Button{
    border: none;
    background-color: rgb(91, 44, 13);
    cursor: pointer;
  }
/*
  svg {
    position: relative;

    transform: translate(0%, 0%);
    color: black;
    
  }
  */
  FaTimes{
    position: relative;
    color: black;
    width: 8%;
    
    
  }
  FaTime:hover{
    cursor: pointer; 
  }
  
  FaSearch{
    width: 3%;
    cursor: pointer;
    
  }


  .search-bar{
    width: 60%;
    
  }
  .search-box{
    width: 90%;
    height: 100%;
    background: white;
  }
`;

export default Search;
