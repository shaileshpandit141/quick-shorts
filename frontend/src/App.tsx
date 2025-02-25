import Routes from "routes/Routes";
import { AddSEO, appMetaConfig } from "SEO";

// App entry point.
const App = (): JSX.Element => {
  return <>
    <AddSEO
      title={appMetaConfig.appName}
      description="Welcome to my website, where you can find the best content."
      keywords="home, react, SEO, optimization"
    />
    <Routes />
  </>;
};

export default App;
