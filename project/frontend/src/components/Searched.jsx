import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';
import ReactCardFlip from 'react-card-flip';
import { FaExternalLinkAlt } from "react-icons/fa";

function Searched() {
  const [searchedRecipes, setSearchedRecipes] = useState([]);
  let params = useParams();
  const [flips, setFlips] = useState([]); const getFlipInitialState = (num) => {
    const initialState = Array(num).fill(false);
    return initialState;
  };

  const getSearched = async (name) => {
    const data = await fetch(`http://localhost:8000/search/?query=${name}`);
    const recipes = await data.json();
    setSearchedRecipes(recipes.results);
    setFlips(getFlipInitialState(recipes.results.length));
  }; useEffect(() => {
    getSearched(params.search);
  }, [params.search]); 
  
  const handleClick = (index) => {
    const newFlips = [...flips];
    newFlips[index] = !newFlips[index];
    setFlips(newFlips);
  }; return (

    <Display> <h1> Displaying Most Relevant Search Results </h1>
  <Grid>
    {searchedRecipes.map((recipe, index) => (<ReactCardFlip
      key={recipe.title}
      isFlipped={flips[index]}
      flipDirection="vertical">
        <FrontCard onClick={() => 
          handleClick(index)}><h3>{index + 1}. {recipe.title}</h3>
          </FrontCard>
        <BackCard onClick={() => 
        handleClick(index)}>
          <h5> {recipe.ingredients}</h5> 
          <a href={"https://"+recipe.link} > <FaExternalLinkAlt/> </a>
         
        </BackCard>
        </ReactCardFlip>
    ))}
    </Grid>
    </Display>
  );
} 

const Display = styled.div`
color: brown;
align-items: center;

`;
const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr));
  grid-gap: 1.5rem;
a{
  color: black'
}
`; 


const Card = styled.div`
  img {
    width: 100%;
    border-radius: 1rem;
  }
  a {
    text-decoration: none;
color:black;
  }
  h4 {
    text-align: center;
    padding: 1rem;
  }
::-webkit-scrollbar {display:none;}
`;

const FrontCard = styled(Card)`
  background: #7B5912;
  color: white;
  height: 300px;
  padding: 20px;
  border-radius: 1rem;
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
a {
      text-decoration: none;
  color:black;
    }
  background: #7B5912;
  color: white;
  height: 300px;
  padding: 20px;
  border-radius: 1rem;
  font-size: 40px;
  font-family: "Ink Free", sans-serif;
  font-weight:600;
  text-align: center;
  margin: 20px;
  cursor: pointer;
overflow-y: scroll;
opacity:0.75;
`; export default Searched;