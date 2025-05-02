import { useAPI } from "../../hooks";

import Typography from '@mui/material/Typography';

function Home() {

  const { data, isLoading, error } = useAPI({ url:'/api/compounds/' }, {});

  return <Typography>{ isLoading ? 'Hello' : error ? 'An error has occurred' : 'Data has loaded!' }</Typography>;
}

export default Home;
