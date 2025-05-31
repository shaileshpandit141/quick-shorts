import React, { FC, JSX } from "react";
import "./ActionButtons.css";
import { Button } from "components";

interface ActionButtonsProps {}

const ActionButtons: FC<ActionButtonsProps> = (props): JSX.Element => {
  return (
    <div className="action-buttons">
      <div className="btn-container">
        <Button type="icon" icon="thumbUp" />
        <label htmlFor="">23K</label>
      </div>
      <div className="btn-container">
        <Button type="icon" icon="thumbDown" />
        <label htmlFor="">5K</label>
      </div>
      <div className="btn-container">
        <Button type="icon" icon="comment" />
        <label htmlFor="">1M</label>
      </div>
    </div>
  );
};

export default ActionButtons;
