import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';

function Searched() {
	const [searchedRecipes, setSearchedRecipes] = useState([]);
	let params = useParams();

	const getSearched = async name => {
		console.log("NAME");
		console.log(name);
		
		const data = await fetch(			
		    `http://localhost:8000/search/?query=${name}`
		);
		const recipes = await data.json();
		console.log("recipes: ",recipes);
		try {
		setSearchedRecipes(recipes.results);
		}
		catch(err){
			console.log("caught err: ",err)
		}
		console.log("after")
		console.log("searched recipes: ",searchedRecipes);		
	};

	useEffect(() => {
		getSearched(params.search);
	}, [params.search]);

	return (
	
		

		<Grid>
		
			{searchedRecipes.map(recipe => {
				return (
					<Link to={`/recipe/${recipe.id}`}>
						<Card key={recipe.title}>
							<h3> {recipe.title} </h3>
							<h4> {recipe.ingredients} </h4>
							<h5>{recipe.directions}</h5>
						</Card>
					</Link>
				);
			})}
		</Grid>
		
		
	);
}
const Grid = styled.div`
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr));
	grid-gap: 3rem;
`;

const Card = styled.div`
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
`;
export default Searched;
