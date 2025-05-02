import { createRoot } from 'react-dom/client';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});


const container = document.getElementById('root');
const root = createRoot(container);

import Home from './components/home';

root.render(
  <ThemeProvider theme={darkTheme}>
    <CssBaseline />
    <Home />
  </ThemeProvider>
);
