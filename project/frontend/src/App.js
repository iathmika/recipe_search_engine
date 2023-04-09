
//import { browserHistory, Router, Route } from 'react-router';

import { BrowserRouter as Router, Link } from "react-router-dom";
import styled from "styled-components";
import { GiKnifeFork } from "react-icons/gi";
import Search from "./components/Search";
import Loader from "./components/Loader";
import logo from "./images/favpng_cooking-cartoon.png";
import Pages from "./components/Pages"
import Category from "./components/Category"

import "./index.css"
import './App.css';
import Button from "./components/Button";
//import Advsearch from "./components/Advsearch"
//import "./Advsearch.css"

/* Add Recipe Search (Chef's Recipes) in a separate div */

function App() {
 
  return (
    
      <Router >
        <LogoWrapper>
            <Logo to="/">
              <img src={logo} alt="" width={60} height={60} />
              Recipe Search 
         
            </Logo>
          
          </LogoWrapper>
         
      <div className="app-wrap">
          
          <div class="app-content">
            <Heading>Being Smart Chef Everyday</Heading>
            <Nav> 
              <Search />
            </Nav>
           
          </div>   
      </div>
         <Pages />
         
          
        
      </Router>
   
  );
}

const LogoWrapper = styled.div`
background: rgb(91, 44, 13);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99;
  padding: 0rem 0;
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  opacity: 80%;
`

const Logo = styled(Link)`
  position: relative; 
  display: flex;
  text-decoration: none;
  text-align: center;
  justify-content: center;
  align-items: center;
  font-size: 1.8rem;
  font-weight: bold;
  font-family: "Ink Free", sans-serif;
  padding-left: 2rem;
  color: white;

  img {
    object-fit: contain;
  }
`;

const Heading = styled.h1`
 padding: 7rem 0 1rem;
 text-align: center;
 color: white;
 font-weight: bold;
`

const Nav = styled.div`
  background-repeat: no-repeat;
  background-size: cover;
  padding: 0 0 8rem;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  svg {
    color: var(--white-600);
    font-size: 2rem;
  }
`;

export default App;
/*
const { useState, useEffect } = React;

const ThemeContext = React.createContext()

// Main component -------------------------------
//const Card = props => {


  const [char, setChar] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPage, setTotalPage] = useState(1);
  const [word, setWord] = useState('a')
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    getData()
  }, []);
  
  const storeInputValue = (value) => {
    console.log(value);
    setWord(value);
  }
  
  const handleNext = () => {
    
    setCurrentPage(prevPage => prevPage + 1);
    getData(currentPage+1, word);
    console.log(currentPage);
    
    // Scroll to top after clicking next/back
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }
  
  const handleBack = () => {
    
    setCurrentPage(prevPage => prevPage - 1);
    getData(currentPage-1, word);
    console.log(currentPage);
    
    // Scroll to top after clicking next/back
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }
  
  const genCards = () => {
    let allCards = [];
    char.map((card, index) => {
      allCards.push(<Card {...card} key={index} />);
    });
    
    return allCards;
  }
  
  let allCards = genCards();
  
  return (
    <div className='main'>
      <div className='head'>
        <img src='https://occ-0-1190-2774.1.nflxso.net/dnm/api/v6/LmEnxtiAuzezXBjYXPuDgfZ4zZQ/AAAABVK-867iNzC3GeSiDQJ7jasFpdN4ySy2Of17S2KxaxbOOtsqax_k_ldd_f5TiDeulU3_lyJmIjtBgPVKLnE1cUK-kRk9yZsO4MXA.png?r=47e' />
      </div>
      <Search 
          getInputValue={storeInputValue} 
          getSubmit={() => getData(1, word)}
          sendEnter={() => getData(1, word)}
          />
      
      <div className='cards'>
        
        {loading ? <Loader /> : 
        (allCards.length === 0 ? <div className='error'>No one found...<i class="far fa-grin-beam-sweat"></i></div> : allCards)}
      </div>
      
      <div className='btns'>
        {currentPage === 1 ? null : <button className='btn back'onClick={handleBack}>Back</button>}
        {currentPage === totalPage ? null : <button className='btn next' onClick={handleNext}>Next </button>}
      </div>
    </div>
  )
}


  
  return (
    <div className='card' data-id={props.id}>
      <img src={props.image || 'https://via.placeholder.com/300x300/111217/FFFFFF/?text=Loading...'} 
        onClick={handleClick}
        alt={props.name} 
        data-id={props.id} />
      
      { showPop &&
        <div className='popup'>
        <article className='popup-content'>
          <i className="popup-close fas fa-times" onClick={handleClick}></i>
          <div className='popup-a'>
            <img src={props.image || 'https://via.placeholder.com/300x300/111217/FFFFFF/?text=Loading...'} 
              alt={props.name} />
          </div>
          <div className='popup-b'>
            <h2>{props.name}</h2>
            
            <div className='popup-details'>
              <span>Gender: </span><span>{props.gender}</span>
            </div>
            <div className='popup-details'>
              <span>Species: </span><span>{props.species}</span>
            </div>
            <div className='popup-details'>
              <span>Status: </span><span>{props.status}</span>
            </div>
            <div className='popup-details'>
              <span>Origin: </span><span>{props.origin ? props.origin.name : '-'}</span>
            </div>
            <div className='popup-details'>
              <span>Location: </span><span>{props.location ? props.location.name : '-'}</span>
            </div>
            
          </div>
        </article>
      </div>
      }
    </div>
  )
}
export default App;
//ReactDOM.render(<Main />, document.getElementById('app'));
*/