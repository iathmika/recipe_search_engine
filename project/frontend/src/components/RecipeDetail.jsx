import styled from 'styled-components';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ReactCardFlip from 'react-card-flip';

//square
const Square = () => {
   return (
     <div style={{ width: '400px', 
      height: '400px', 
      backgroundColor: 'red', 
      margin: 'auto' ,
      borderRadius: '10px',
      // display: 'flex', 
      // justifyContent: 'center', 
      // alignItems: 'center',
      boxShadow: '0 0 10px rgba(0, 0, 0, 0.5)',
      background: 'grey'
   }}>
   </div>
   );
 };

//recommender fetcher

//recommender function
// function Recommender(){
//    return(
//    <Display2>
//       <h1>Recommended Values</h1>
//       {/* <Square>
      
//       </Square> */}
//    </Display2>
//    )
// }


function Recommendations(id) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async (id) => {
      //fetch the data
      const response = await fetch(`http://localhost:8000/recommendations/?recipe_id=14`);
      //store the data
      const responseData = await response.json();
      setData(responseData.results);
    };
    fetchData();
  }, []);

  if (!data) {
    return <div>No recommendations</div>;
  }

  return (
    <div>
      <h1>You may also like</h1>
      <ul>
        {data.map((recommendation, index) => (
          <li key={index}>{recommendation.title}</li>
        ))}
      </ul>
    </div>
  );
}

// nutrition function
function NutritionCalculator(){


   return(
   <Display2>
      <h1>Nutrition Values</h1>
      <Square/>
   </Display2>
   )
}

// below function is used to display the title, ingredients and recipe of the dish
function RecipeDetail() {
   const [recipeName, setRecipeName] = useState('')
   const [recipeDirections, setRecipeDirections] = useState('[]')
   const [recipeIngredients, setRecipeIngredients] = useState('[]')
   useEffect(()=>{

      let params = window.location.href
      params = params.split('?')[1]
      params = params.split('&')
      // setRecipeName(params[0].split('=')[1].replaceAll('%20',' ').replaceAll('%27',''))
      console.log(params)
      setRecipeName(params[0].split('=')[1].replaceAll('%20',' ').replaceAll('%27','').replaceAll('%22',''))
      let directions = decodeURIComponent(params[1].split('=')[1])
      setRecipeDirections(directions.trim().slice(1,directions.trim().length-1))
      let ingredients = decodeURIComponent(params[2].split('=')[1])
      setRecipeIngredients(ingredients.trim().slice(1,ingredients.trim().length-1))
      let id = parseInt(decodeURIComponent(params[3].split('=')[1]))
      console.log(id)

   },[recipeIngredients])
   return (
      <Display>
         <Div>
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
         </Div>
         <Div2>
            <NutritionCalculator/>
            <br></br>
            <Recommendations/>
         </Div2>

      </Display>
   );
}

const Display = styled.div`
color: brown;
/*align-items: center;*/
display:flex;
/*width: 50%;*/
`;

const Div = styled.div`
width:50%;
`;
const Div2 = styled.div`
float:right;
align-items: left;
width:50%;
`;

const Display2 = styled.div`
color: brown;
align-items: center;
/*float: right;*/
/*width: 50%;*/
`;

const Grid = styled.div`

`; 

export default RecipeDetail;