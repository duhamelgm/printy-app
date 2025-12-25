import { goto } from "$app/navigation";
import { PUBLIC_API_URL } from "$env/static/public";

const authorizedPost = async (path: string, body: any) => {
  const response = await fetch(`${PUBLIC_API_URL}${path}`, {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('authToken') || ''
    }
  });
  
  const data = await response.json();
  if (!('status' in data)) {
    throw new Error('Invalid response');
  }

  if (data.status === 'error') {
    if (data.message === 'Unauthorized') {
      goto('/login');
      localStorage.removeItem('authToken');
      return
    }

    throw new Error(data.message);
  }

  return data;
};

export default authorizedPost;