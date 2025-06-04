import React, { FC, JSX } from "react";
import "./UserPage.css";
import { Button } from "components";

interface UserPageProps {}

const UserPage: FC<UserPageProps> = (props): JSX.Element => {
  return (
    <div className="user-page">
      <section className="header-section">
        <figure className="figure-container">f</figure>
        <h5 className="username">Username</h5>
      </section>
      <section className="shorts-posted-section">
        <div className="filters-section">
          <Button type="button">Shorts</Button>
          <Button type="button">Others</Button>
        </div>
        <div className="shorts-posted-container">
          <div className="scroll-container">
            {Array(8)
              .fill(0)
              .map((_, index) => (
                <div className="video-crad" key={index}>
                  {index}
                  {/* <video
                  src="http://localhost:8000/api/v1/shorts/videos/streams/3/"
                >
                  Your Browser is not supported the video tag
                </video> */}
                </div>
              ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default UserPage;
