import useFormDataChange from "hooks/useFormDataChange"

interface FormData {
  email: string;
  password: string;
}

interface FormField {
  name: string;
  type: 'email' | 'password' | 'checkbox';
  value: string | boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

type FormFields = FormField[];

const useSigninFormFields = (): [FormFields, FormData] => {
  const [formData, handleFormDataChange] = useFormDataChange<FormData>({
    email: '',
    password: ''
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
    }
  ]

  return [formFields, formData]
}

export default useSigninFormFields
