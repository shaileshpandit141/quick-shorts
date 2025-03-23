import React from "react";
import "./HomePage.css";
import { AddSEO } from "SEO";

const HomePage: React.FC = (props) => {
  return (
    <div className="grid-12 home-page">
      <AddSEO
        title="Home"
        description="Welcome to my website, where you can find the best content."
        keywords="home, react, SEO, optimization"
      />
      <div className="grid-start-2-end-2 content">
        <h1>Welcome to my website</h1>
        <p>
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Amet quod
          soluta officia molestias recusandae asperiores est perferendis
          dolorum! Id reiciendis fugiat laboriosam doloremque quae ratione iusto
          enim, cumque atque magni.
        </p>
      </div>
    </div>
  );
};

export default HomePage;
