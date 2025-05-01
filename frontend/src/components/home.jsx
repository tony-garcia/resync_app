import { useAPI } from "../../hooks";

function Home() {

  const { data, isLoading, error } = useAPI({ url:'/api/compounds/' }, {});

  return <p>{ isLoading ? 'Hello' : error ? 'An error has occurred' : 'Data has loaded!' }</p>;
}

export default Home;
