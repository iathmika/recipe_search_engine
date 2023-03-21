import styled from 'styled-components';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

function RecipeDetail() {
   const [recipeName, setRecipeName] = useState('')
   const [recipeDirections, setRecipeDirections] = useState('[]')
   const [recipeIngredients, setRecipeIngredients] = useState('[]')

   const getRecommended = async (name) => {
    const data = await fetch(`http://localhost:8000/getRecommendations/query=""`);
    //const 
}
    const recommendedRecipes = fetch();
   useEffect(()=>{
      let params = window.location.href
      params = params.split('?')[1]
      params = params.split('&')
      setRecipeName(params[0].split('=')[1].replaceAll('%20',' ').replaceAll('%27',''))
      let directions = decodeURIComponent(params[1].split('=')[1])
      setRecipeDirections(directions.trim().slice(1,directions.trim().length-1))
      let ingredients = decodeURIComponent(params[2].split('=')[1])
      setRecipeIngredients(ingredients.trim().slice(1,ingredients.trim().length-1))
   },[recipeIngredients])
   return (
      <Display>
         <h1> {recipeName} </h1>
         <Grid>
            <h2>Ingredients</h2>
            <ul>
               {JSON.parse(recipeIngredients).map(
                  (ingredient) => (<li>{ingredient}</li>)
               )}
            </ul>
            <h2>Directions</h2>
            <ul>
               {JSON.parse(recipeDirections).map(
                  (direction) => (<li>{direction}</li>)
               )}
            </ul>
         </Grid>
      </Display>
   );
}

const Display = styled.div`
color: brown;
align-items: center;
`;

const Grid = styled.div`

`; 

export default RecipeDetail;