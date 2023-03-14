import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';
import ReactCardFlip from 'react-card-flip'; function Searched() {
  const [searchedRecipes, setSearchedRecipes] = useState([]);
  let params = useParams();
  const [flips, setFlips] = useState([]);   const getFlipInitialState = (num) => {
    const initialState = Array(num).fill(false);
    return initialState;
  };   const getSearched = async (name) => {
    const data = await fetch(`http://localhost:8000/search/?query=${name}`);
    const recipes = await data.json();
    setSearchedRecipes(recipes.results);
    setFlips(getFlipInitialState(recipes.results.length));
  };   useEffect(() => {
    getSearched(params.search);
  }, [params.search]);   const handleClick = (index) => {
    const newFlips = [...flips];
    newFlips[index] = !newFlips[index];
    setFlips(newFlips);
  };return (<Grid>
      {searchedRecipes.map((recipe, index) => (<ReactCardFlip
          key={recipe.title}
          isFlipped={flips[index]}
          flipDirection="vertical"><FrontCard onClick={() => handleClick(index)}><h3>{index+1}. {recipe.title}</h3><h4>{recipe.ingredients}</h4></FrontCard><BackCard onClick={() => handleClick(index)}><h5>* {recipe.directions}</h5></BackCard></ReactCardFlip>
      ))}</Grid>
  );
} const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr));
  grid-gap: 3rem;
`; const Card = styled.div`
  img {
    width: 100%;
    border-radius: 2rem;
  }
  a {
    text-decoration: none;
  }
  h4 {
    text-align: center;
    padding: 1rem;
  }
::-webkit-scrollbar {display:none;}
`; const FrontCard = styled(Card)`
  background: brown;
  color: white;
  height: 500px;
  padding: 20px;
  border-radius: 4rem;
  font-size: 40px;
  font-family: "Ink Free", sans-serif;
  font-weight:600;
  text-align: center;
  margin: 20px;
  cursor: pointer;
overflow-y: scroll;
  opacity:0.75;
`; 
const BackCard = styled(Card)`
  background: brown;
  color: white;
  height: 500px;
  padding: 20px;
  border-radius: 4rem;
  font-size: 40px;
  font-family: "Ink Free", sans-serif;
  font-weight:600;
  text-align: center;
  margin: 20px;
  cursor: pointer;
overflow-y: scroll;
opacity:0.75;
`; export default Searched;