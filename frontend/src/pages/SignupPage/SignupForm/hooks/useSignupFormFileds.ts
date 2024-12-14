import useFormDataChange from "hooks/useFormDataChange"

interface FormData {
  email: string;
  password: string;
  confirm_password: string;
}

interface FormField {
  name: string;
  type: 'email' | 'password' | 'checkbox';
  value: string | boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

type FormFields = FormField[];

const useSignupFormFields = (): [FormFields, FormData] => {
  const [formData, handleFormDataChange] = useFormDataChange<FormData>({
    email: '',
    password: '',
    confirm_password: ''
  })

  const formFields: FormFields = [
    {
      name: 'email',
      type: 'email',
      value: formData.email,
      onChange: handleFormDataChange
    },
    {
      name: 'password',
      type: 'password',
      value: formData.password,
      onChange: handleFormDataChange
    },
    {
      name: 'confirm_password',
      type: 'password',
      value: formData.confirm_password,
      onChange: handleFormDataChange
    }
  ]
  
  return [formFields, formData]
}

export default useSignupFormFields
