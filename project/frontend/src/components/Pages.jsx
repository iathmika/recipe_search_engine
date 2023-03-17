import React from 'react';
import Home from './Home';
import { Route, Routes, useLocation } from 'react-router-dom';
import Cuisine from './Cuisine';
import Searched from './Searched';
import Recipe from './Recipe';
import RecipeDetail from './RecipeDetail';
import { AnimatePresence } from 'framer-motion';

function Pages() {
	const location = useLocation();
	return (
		<AnimatePresence mode='wait'>
			<Routes location={location} key={location.pathname}>
				
				
				<Route path="/searched/:search" element={<Searched />} />
				<Route path="/recipe-detail/:search" element={<RecipeDetail />} />
				<Route path="/recipe/:name" element={<Recipe />} />

			</Routes>
		</AnimatePresence>
	);
}

export default Pages;
