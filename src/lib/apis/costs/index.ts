import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getCostData = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/api/v1/costs`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      error = err;
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const createCostRecord = async (token: string, costData: object) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/api/v1/costs`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(costData)
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      error = err;
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const updateCostRecord = async (token: string, costId: string, costData: object) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/api/v1/costs/${costId}`, {
    method: 'PUT',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(costData)
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      error = err;
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};
