import React from "react";
import "./DisplaySuccessDetails.css";

interface Props {
  details: string | string[] | undefined;
}

const DisplaySuccessDetails: React.FC<Props> = ({ details }) => {
  if (details === undefined) {
    return null;
  }

  if (typeof details === "string") {
    return (
      <div className="success-details-container">
        <p className="detail">{details}</p>
      </div>
    );
  }

  return (
    <div className="success-details-container">
      {details.map((detail, index) => (
        <p className="detail" key={index}>
          {detail}
        </p>
      ))}
    </div>
  );
};

export default DisplaySuccessDetails;
