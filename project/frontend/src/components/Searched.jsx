import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';
import ReactCardFlip from 'react-card-flip';
import { FaExternalLinkAlt } from "react-icons/fa";
import RecipeDetail from './RecipeDetail';
import { useNavigate } from "react-router-dom";

function Searched() {
  const [searchedRecipes, setSearchedRecipes] = useState([]);
  let params = useParams();
  const [flips, setFlips] = useState([]);
  const [recipeCardClick, setRecipeCardClick] = useState(false);
  const [recipeName, setRecipeName] = useState('')
  const [recipeIngredients, setRecipeIngredients] = useState(null)
  const [recipeDirections, setRecipeDirections] = useState(null)
  const getFlipInitialState = (num) => {
    const initialState = Array(num).fill(false);
    return initialState;
  };

  const navigator = useNavigate();
  const getSearched = async (name) => {
    const data = await fetch(`http://localhost:8000/search/?query=${name}`);
    
    const recipes = await data.json();

    console.log("recipes length: ",recipes.results.length);
    
    setSearchedRecipes(recipes.results);
    setFlips(getFlipInitialState(recipes.results.length));
  }; 
  
  useEffect(() => {
    getSearched(params.search);
  }, [params.search]);
  
  const handleClick = (index, type, recipeTitle, recipeIngredients, recipeDirections) => {
    if(type == "back"){
      
      setRecipeCardClick(true)
      setRecipeName(recipeTitle)
      setRecipeIngredients(recipeIngredients)
      setRecipeDirections(recipeDirections)
      const updatedRecipeTitle = recipeTitle.replaceAll(" ", '-')
      const recipeData = {
        recipeTitle: updatedRecipeTitle,
        recipeDirection: recipeDirections,
        recipeIngredients: recipeIngredients,
      };
      /*
      fetch(`/recipeDetail/${updatedRecipeTitle}/` ,{
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          // handle response data

        })
        .catch(error => {
          console.error('Error:', error);
        });
        */
      navigator(`/recipe-detail/${updatedRecipeTitle}?recipeTitle='${recipeTitle}&recipeDirection='${recipeDirections}'
      &recipeIngredients='${recipeIngredients}'`);
     //http://localhost:3000/recipe-detail/$%7BupdatedRecipeTitle%7D/
     //http://localhost:3000/recipe-detail/Vanilla-Ice-Cream/
    }
    const newFlips = [...flips];
    newFlips[index] = !newFlips[index];
    setFlips(newFlips);
  }; 
  //console.log("searched recipes: ",searchedRecipes);
  //console.log("searched recipes length: ",searchedRecipes.length);
  //console.log("type of recipes: ", typeof searchedRecipes);
   
    //console.log("returning cards");

  if(!(searchedRecipes.length)){
    return (
    <h1> </h1> 
    );
  }
  else {
  return (
      <Display> 
        <h1> {recipeName !== '' ? recipeName : 'Here are your recipes'} </h1>
        <Grid>
          {searchedRecipes.map((recipe, index) => (
          <ReactCardFlip
            key={recipe.title}
            isFlipped={flips[index]}
            flipDirection="vertical">
              <FrontCard 
              onClick={() => 
                handleClick(index,"front",'')}
              >
                  <h3>{index + 1}. {recipe.title}</h3>
              </FrontCard>
              <BackCard 
              onClick={() => handleClick(index,"back",recipe.title, recipe.ingredients, recipe.directions)}
              onMouseLeave={() => handleClick(index,"front",'')}
              >
                
                <h5> 
                  <ul>
                    {JSON.parse(recipe.ingredients).map(
                        (ingredient) => (<li>{ingredient}</li>)
                    )}
                  </ul>
                 </h5> 
                 <h5>Click to get directions</h5>
              </BackCard>
            </ReactCardFlip>
          ))}
          
        </Grid>
      </Display>
  );
} }

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
  padding: 85px;
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
const Heading = styled.h1`
  font-size: 2.5rem;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif';
  text-align: center;
  margin-bottom: 2rem;
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
  text-align: left;
  margin: 20px;
  cursor: pointer;
overflow-y: scroll;
opacity:0.75;
`; 

export default Searched;