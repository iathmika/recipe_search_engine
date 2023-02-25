import styled from "styled-components";
import { FaSearch } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import image from "../images/bg.jpeg";
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

  return (
    <FormStyle onSubmit={submitHandler}>
      <div>
        <FaSearch />
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </div>
    </FormStyle>
  );
}

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
    position: relative;
    width: 100%;
  
    max-width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  input {
    border: none;
    background: linear-gradient(35deg, #494949, #313131);
    font-size: 2rem;
    color: white;
    padding: 1rem 3rem;
    border-radius: 1rem;
    outline: none;
    width: 80%;
    opacity: 0.33;
  }

  svg {
    position: absolute;
    top: 50%;
    left: 5% ;
    transform: translate(50%, -50%);
    color: white;
    
  }
`;

export default Search;
