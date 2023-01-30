import callToBackend from "./apiHandler";
import { API_PATH } from "./apiPaths";


// Get all posts
export const getAllPost = async () => {
  return await callToBackend('GET', API_PATH.ALL_POSTS);
};

// Get delete a post
export const deleteAPost = async (id, headers) => {
  return await callToBackend('POST', API_PATH.DELETE_A_POST, null, id, headers);
};
// Get all posts  
export const getMyPosts = async (headers) => {
  return await callToBackend('GET', API_PATH.MY_POSTS, null, null, headers);
};

export const signIn = async (payload, headers) => {
  return await callToBackend('POST', API_PATH.SIGNIN, null, payload, headers);
};