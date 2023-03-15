import styled from "styled-components";
import { FaSearch } from "react-icons/fa";
import { FaTimes } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import image from "../images/bg.jpeg";
import Button from "./Button"
import React from "react";


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
              autofocus 
              required
            />
            <button class="cross-btn">
              <FaTimes onClick={handleClearBtn}/>
            </button>
          </div>
          {/* Search Logo */}
          <button class="search-btn">
            <FaSearch onClick={submitHandler} /> 
          </button>
        </div>
      
        
        
        
    </FormStyle> 
 

  )
}

const FormStyle = styled.form`
  position: relative;
  margin: 0 auto;
  width: max-content;
  display: flex;
  justify-content: center;
  align-items: center;

  .fa-times:hover {
    cursor: pointer;
  }
 
  input {
    border: 0;
    position: relative;
    background: transprent;
    font-size: 1rem;
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

  button {
    border: none;
    background-color: rgb(91, 44, 13);
    cursor: pointer;
    color: white;
  }

/*
  svg {
    position: relative;

    transform: translate(0%, 0%);
    color: black;
    
  }
  
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
  */

  .search-bar {
    width: 100%;
    min-width: 50vw;
    display: flex;
    align-items: center;
    background: white;
    border: none;
    padding: 0;
    border-radius: 0.25rem;
    overflow: hidden;
  }

  .search-box {
    height: 100%;
    width: 90%;
    background: white;
    position: relative;
  }

  .cross-btn {
    position: absolute;
    right: 0;
    height: 100%;
    top: 0;
    background: none;
    color: black;
    padding: 0 0.5rem;

    svg {
      width: 24px;
      height: 24px;
    }
  }

  .search-btn {
    display:flex;
    align-items:center;
    justify-content:center;
    padding: 1rem;
    position: relative;
    width: 10%;

    svg {
      width: 24px;
      height: 24px;
    }
  }
`;

export default Search;
