export const get_absolute_url = (
  relative_url: string | null | undefined
): string => {
  /** Base API URL from environment variables */
  const BASE_API_URL = process.env.REACT_APP_BASE_API_URL || ''

  if (typeof relative_url === 'string') {
    // Handle trailing slash in base URL to avoid double slashes
    const baseUrl = BASE_API_URL.endsWith('/') ? BASE_API_URL.slice(0, -1) : BASE_API_URL
    return `${baseUrl}/${relative_url.replace(/^\//, '')}`
  } else {
    return BASE_API_URL.endsWith('/') ? BASE_API_URL.slice(0, -1) : BASE_API_URL
  }
}
