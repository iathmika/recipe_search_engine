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
		//const recipes = await data.json();
		setSearchedRecipes(data);		
	};

	useEffect(() => {
		getSearched(params.search);
	}, [params.search]);

	return (
		<Grid> </Grid>
		/*

		<Grid>
		
			{searchedRecipes.map(recipe => {
				return (
					<Link to={`/recipe/${recipe.id}`}>
						<Card key={recipe.id}>
							<img src={recipe.image} alt={recipe.title} />
							<h4>{recipe.title}</h4>
						</Card>
					</Link>
				);
			})}
		</Grid>
		*/
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
