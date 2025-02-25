import React, { useState, ChangeEvent } from "react";
import "./Input.css";
import Button from "components/Button/Button";
import DisplayFormErrors from "../DisplayFormErrors/DisplayFormErrors";
import { Errors } from "FeatureTypes";

type InputType =
  | "text"
  | "password"
  | "email"
  | "url"
  | "search"
  | "tel"
  | "number"
  | "date"
  | "datetime-local"
  | "month"
  | "week"
  | "time"
  | "checkbox";

interface InputProps {
  name: string;
  type: InputType;
  value: string | number | boolean;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  readOnly?: boolean;
  errors?: Errors[];
  isRequired?: boolean;
  isDisabled?: boolean;
}

const Input: React.FC<InputProps> = ({
  name,
  type,
  value,
  onChange,
  isRequired = true,
  isDisabled = false,
  readOnly = false,
  errors = [],
}) => {
  const [isPasswordShow, setIsPasswordShow] = useState(false);
  const id = `${name}${type}`;
  const formattedLabel = name.replace(/_/g, " ");

  const renderInputElement = (inputType: string, additionalProps = {}) => (
    <input
      name={name}
      type={inputType}
      id={id}
      onChange={onChange}
      required={isRequired}
      disabled={isDisabled}
      readOnly={readOnly}
      className="input"
      {...additionalProps}
    />
  );

  const renderPasswordToggle = () => (
    <div className="show-password-icon-container">
      <Button
        type="icon"
        className="password-show-hide-button"
        icon={isPasswordShow ? "eyeOpen" : "eyeClose"}
        onClick={() => setIsPasswordShow((prev) => !prev)}
      />
    </div>
  );

  if (type === "checkbox") {
    return (
      <div className="input-checkbox-component">
        <div className="input-element-wrapper">
          <div className="input-element">
            {renderInputElement(type, { checked: Boolean(value) })}
            <label htmlFor={id} className="label">
              <span>{formattedLabel}</span>
            </label>
          </div>
        </div>
        <DisplayFormErrors field={name} errors={errors} />
      </div>
    );
  }

  const inputType =
    type === "password" ? (isPasswordShow ? "text" : "password") : type;
  const inputValue = typeof value !== "boolean" ? value : String(value);

  return (
    <div className="input-component">
      <div className="input-element-wrapper">
        <div className="input-element">
          {renderInputElement(inputType, {
            value: inputValue,
            placeholder: "",
            autoComplete: "off",
          })}
          <label htmlFor={id} className="label">
            <span>{formattedLabel}</span>
          </label>
        </div>
        {type === "password" && renderPasswordToggle()}
      </div>
      <DisplayFormErrors field={name} errors={errors} />
    </div>
  );
};

export default Input;
