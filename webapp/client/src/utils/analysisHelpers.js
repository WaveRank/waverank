// Takes raw genre object and returns sorted array of [name, value] pairs
export const prepareGenreData = (data, fileName) => {
    const genreData = data[fileName] || {};
    return Object.entries(genreData).sort((a, b) => b[1] - a[1]);
};

// Maps decimal value to color from Magma palette (for bar graph)
export const getMagmaColor = (val) => {
    if (val > 0.8) return '#fcfdbf'; 
    if (val > 0.6) return '#feb078'; 
    if (val > 0.4) return '#f1605d'; 
    if (val > 0.2) return '#b73779'; 
    if (val > 0.1) return '#721f81'; 
    return '#2c115f';              
};

// Converts decimal to percentage
export const formatPercentage = (value) => {
    return (value * 100).toFixed(1);
};