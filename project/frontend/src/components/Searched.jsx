import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';
import ReactCardFlip from 'react-card-flip';
import { FaExternalLinkAlt } from "react-icons/fa";
import RecipeDetail from './RecipeDetail';
import { useNavigate } from "react-router-dom";
// import Advsearch from "./Advsearch"
// import "./Advsearch.css"  
// import ReactPaginate from 'react-paginate';

function Searched() {
  const [searchedRecipes, setSearchedRecipes] = useState([]);
  let params = useParams();
  const [flips, setFlips] = useState([]);
  const [recipeCardClick, setRecipeCardClick] = useState(false);
  const [recipeName, setRecipeName] = useState('');
  const [recipeIngredients, setRecipeIngredients] = useState(null);
  const [recipeDirections, setRecipeDirections] = useState(null);
  const [recipeNER, setRecipeNER] = useState(null);
  const [query, setQuery] = useState(null);
  const getFlipInitialState = (num) => {
    const initialState = Array(num).fill(false);
    return initialState;
  };

  const navigator = useNavigate();
  const getSearched = async (input) => {
    console.log("type: ");
    // console.log(Advsearch.searchtype);
    const params = input.split("&");
    const name = params[0];
    setQuery(name);
    const type = params[1];
    const data = await fetch(`http://localhost:8000/search/?query=${name}&search_type=${type}`);
    
    const recipes = await data.json();

    console.log("Recipes:", recipes)
    
    console.log("recipes : ",recipes);
    // console.log("recipes length: ",recipes.results);

    
    setSearchedRecipes(recipes.results);
    setFlips(getFlipInitialState(recipes.results.length));
  }; 

  
  useEffect(() => {
    getSearched(params.search);
  }, [params.search]);
  
  const handleClick = (index, type, id, recipeTitle, recipeIngredients, recipeDirections,recipeNER) => {
    if(type == "back"){
      
      setRecipeCardClick(true)
      setRecipeName(recipeTitle)
      setRecipeIngredients(recipeIngredients)
      setRecipeNER(recipeNER)
      console.log("recipeNER: "+recipeNER)
      setRecipeDirections(recipeDirections)
      // const updatedRecipeTitle = recipeTitle.replaceAll(" ", '-')
      const updatedRecipeTitle = recipeTitle.replaceAll(" ", '-').replaceAll("/", "")
      const recipeData = {
        recipeID : id,
        recipeTitle: updatedRecipeTitle,
        recipeDirection: recipeDirections,
        recipeIngredients: recipeIngredients,
        recipeNER: recipeNER,
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
      navigator(`/recipe-detail/${updatedRecipeTitle}?recipeTitle='${recipeTitle}'&recipeDirection='${recipeDirections}'
      &recipeIngredients='${recipeIngredients}'&recipeID='${id}'&recipeNER='${recipeNER}'`);
     //http://localhost:3000/recipe-detail/$%7BupdatedRecipeTitle%7D/
     //http://localhost:3000/recipe-detail/Vanilla-Ice-Cream/
    }
    const newFlips = [...flips];
    newFlips[index] = !newFlips[index];
    setFlips(newFlips);
  }; 
  
    

  if(searchedRecipes == null){
    // console.log("Hello!!!!!!!!!!");
    return (
    <h1> </h1> 
    );
  }
  else {
    console.log("recipe.NER is "+ searchedRecipes.NER);
  return (
      <Display> 
        <h1> Showing Search Results for "{query}" </h1>

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
                {/* <Image> <img src="https://cdn.iconscout.com/icon/premium/png-128-thumb/recipe-book-2844299-2365212.png"></img>
                </Image> */}
                  <h3 style={{ paddingTop: '115px' }}>{index + 1}. {recipe.title}</h3>
              </FrontCard>
              
              <BackCard 
             
              onClick={() => handleClick(index,"back", recipe.id, recipe.title, recipe.ingredients, recipe.directions, recipe.NER)}
              onMouseLeave={() => handleClick(index,"front",'')}
              >               
                <h6> 
                  <ul>
                    {JSON.parse(recipe.ingredients).map(
                        (ingredient) => (<li>{ingredient}</li>)
                    )}
                  </ul>
                 </h6> 
                 <h5>Click to get directions</h5>
              </BackCard>
            </ReactCardFlip>
          ))}
          
        </Grid>
      </Display>
  );
} }

const Display = styled.div`
color: white;
align-items: center;
h1{
  text-align: center;
}
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr));
  grid-gap: 1.5rem;
align-items: center;
a{
  color: black;
}
`; 
// const Image = styled.div`

// margin-left: 20px;
// margin-right: 20px;
// width: 40%;
// place-items: center;
// align-items: center;
// display: block;
// margin: auto;
// `

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
a {
      text-decoration: none;
  color:black;
    }
  border: 1px solid;
  background: #7B5912;

  height: 350px;
  padding: 25px;
  border-radius: 1rem;
  font-size: 40px;
  font-family: "Ink Free", sans-serif;
  font-weight:600;
  text-align: center;
align-items: center;
  margin: 10px;
  cursor: pointer;
overflow-y: scroll;
  opacity:0.75;
  border: 1px solid;
  transform-style: preserve-3d;
  transition: -webkit-transform ease 500ms;
  transition: transform ease 500ms;
  box-shadow: 10px 10px 5px rgb(95, 77, 99);
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
  border: 1px solid;
  background: #7B5912;
  color: white;
  height: 350px;
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
transform-style: preserve-3d;
transition: -webkit-transform ease 500ms;
transition: transform ease 500ms;
box-shadow: 10px 10px 5px rgb(95, 77, 99);
h5{
  text-align: center;
  text-shadow: 1px 1px 1px #919191,
        1px 2px 1px #919191,
        1px 3px 1px #919191,
        1px 4px 1px #919191,
    1px 8px 6px rgba(16,16,16,0.4),
    1px 1px 1px rgba(16,16,16,0.2),
    1px 8px 5px rgba(16,16,16,0.2),
    1px 1px 1px rgba(16,16,16,0.4);
}

`; 

export default Searched;
