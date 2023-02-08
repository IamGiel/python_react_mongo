import axios from 'axios';

export const callToBackend = async (method, url, params, requestObject, headers) => {
  const config = { method, url, data: requestObject, headers, params };
  console.log(config)
  return axios
    .request({ ...config })
    .then(response => {
      if (!response || response.status !== 200) {
        return Promise.reject();
      }
      console.log("asdasdasdasdsad ", response)
      return Promise.resolve(response?.data?.data?.content ?? response?.data?.data ?? response?.data ?? response);
    })
    .catch(error => {
      return Promise.reject(error?.response?.data);
    });
};
export default callToBackend;
