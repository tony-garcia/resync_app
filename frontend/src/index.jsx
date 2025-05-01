import { createRoot } from 'react-dom/client';

const container = document.getElementById('root');
const root = createRoot(container);

import Home from './components/home';

root.render(
  <Home />
);
