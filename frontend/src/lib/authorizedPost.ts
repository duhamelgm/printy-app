import { goto } from "$app/navigation";
import { PUBLIC_API_URL } from "$env/static/public";

const authorizedPost = async (path: string, body?: any, contentType: 'json' | 'form-data' = 'json') => {
  const response = await fetch(`${PUBLIC_API_URL}${path}`, {
    method: 'POST',
    body: contentType === 'json' ? JSON.stringify(body) : body,
    headers: {
      'Authorization': localStorage.getItem('authToken') || '',
      ...(contentType === 'json' ? { 'Content-Type': 'application/json' } : {}),
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