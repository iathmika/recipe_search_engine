import styled from 'styled-components';
import { useParams, useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ReactCardFlip from 'react-card-flip';

//square
const Square = (nutrition) => {
   console.log("Nutrition square: ",nutrition);
   console.log("Type of Nutrition: ",typeof nutrition);
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
     <h2>Ingredient</h2>
               <ul>
                  {nutrition.map(
                     (vals) => ( <h1>{vals.food_name}</h1>
                  ))}
               </ul>
            
   </div>
   );
 };


function Recommendations(props) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async (id) => {
      //fetch the data
      id = id.replace(/\D/g,'');
      console.log(id);
      const response = await fetch(`http://localhost:8000/recommendations/?recipe_id=${id}`);
      //store the data
      const responseData = await response.json();
      setData(responseData.results);
    };
    fetchData(props.id);
  }, [props.id]);

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
function NutritionCalculator(props){
   const [nutrition, setNutrition] = useState("");

   useEffect(() => {
   const getNutrition = async (NER) => {
      console.log("NER is ");
      console.log(NER);
      NER = NER.replace(/\'/g,'');
      const data = await fetch(`http://localhost:8000/nutrition/?ingredient=${NER}`);
      const nutrition_vals = await data.json();     
      console.log("Nutrition : ",nutrition_vals);
      console.log("nutrition results length ",nutrition_vals.results);
     
      setNutrition(nutrition_vals.results);
      //setFlips(getFlipInitialState(recipes.results.length));
      console.log("Nutrition state: ", nutrition)
    }; 
    getNutrition(props.NER);
   }, [props.NER]);

   if(!(nutrition.length)){
      return (
      <h1> Loading... </h1> 
      );
    }
   else{
   return(
   <Display2>
      <h1>Nutrition Values are: </h1>

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
     <h6>Ingredient</h6>
         {nutrition.map(
            (vals) => ( <ul>{vals.food_name}</ul>
         ))}
   
   </div>

   </Display2>
   );
         }
}

// below function is used to display the title, ingredients and recipe of the dish
function RecipeDetail() {
   const [recipeName, setRecipeName] = useState('')
   const [recipeDirections, setRecipeDirections] = useState('[]')
   const [recipeIngredients, setRecipeIngredients] = useState('[]')
   const [urlParams, setUrlParams] = useState({directions:null, id:null, ingredients:null, NER:null})
   const searchParams = useSearchParams()

   useEffect(() => {

      if (searchParams.length > 0) {
         const queryParams = searchParams[0]
         const directions = queryParams.get('recipeDirection')
         const title = queryParams.get('recipeTitle')
         const ingredients = queryParams.get('recipeIngredients')
         const id = queryParams.get('recipeID')
         const NER = queryParams.get('recipeNER');
         console.log("NER inside RecipeDetail: ");
         console.log(NER);
         

         setUrlParams({
            title: title.replaceAll('%20',' ').replaceAll('%27','').replaceAll('%22',''),
            directions: directions.trim().slice(1,directions.trim().length-1),
            ingredients: ingredients.trim().slice(1, ingredients.trim().length - 1),
            id,
            NER
         })
      }

      // let params = window.location.href
      // params = params.split('?')[1]
      // params = params.split('&')
      // // setRecipeName(params[0].split('=')[1].replaceAll('%20',' ').replaceAll('%27',''))
      // console.log(params)
      // setRecipeName(params[0].split('=')[1].replaceAll('%20',' ').replaceAll('%27','').replaceAll('%22',''))
      // let directions = decodeURIComponent(params[1].split('=')[1])
      // setRecipeDirections(directions.trim().slice(1,directions.trim().length-1))
      // let ingredients = decodeURIComponent(params[2].split('=')[1])
      // setRecipeIngredients(ingredients.trim().slice(1,ingredients.trim().length-1))
      // let id = parseInt(decodeURIComponent(params[3].split('=')[1]))
      // console.log(id)

   }, [])

   return (
      <Display>
         <Div>
            <h1> {urlParams.title} </h1>
            <Grid>
               <h2>Ingredients</h2>
               <ul>
                  {urlParams.ingredients ?JSON.parse(urlParams.ingredients).map(
                     (ingredient) => (<li>{ingredient}</li>)
                  ):null}
               </ul>
               <h2>Directions</h2>
               <ul>
                  {urlParams.directions ? JSON.parse(urlParams.directions).map(
                     (direction) => (<li>{direction}</li>)
                  ):null}
               </ul>
            </Grid>
         </Div>
         
         <Div2>
         
           {urlParams.NER && <NutritionCalculator NER={urlParams.NER}/> }
            <br></br>
            {urlParams.id && <Recommendations id={urlParams.id} />}
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