import React, { useEffect, useState } from "react";
import { View, ActivityIndicator, StyleSheet, Text, Platform } from "react-native"; // Import Text
import { Circle, Svg } from "react-native-svg";
import { Picker } from "@react-native-picker/picker";


const fetchStationData = async (station) => {
  try {
    const response = await fetch(
      `http://192.168.0.27:5000/api/station/${encodeURIComponent(station)}`
    );
    if (!response.ok) throw new Error("Network response was not ok");
    return await response.json();
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
    throw error; // Rethrow the error for handling in the calling context
  }
};

const TubeMap = () => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [startStation, setStartStation] = useState('');
  const [endStation, setEndStation] = useState('');

  if (stations.length > 0 && !startStation) {
    // Initialize start and end stations once the stations are loaded
    setStartStation(stations[0][0]); // Assuming the first element is the station name
    setEndStation(stations[0][0]);
  }

  useEffect(() => {
    fetch("http://192.168.0.27:5000/api/stations?zone=1")
      .then((response) => response.json())
      .then(async (stationNames) => {
        const stationDetails = await Promise.all(
          stationNames.map(fetchStationData)
        );
        setStations(stationDetails);
      })
      .catch((error) => console.error("Error fetching data:", error))
      .finally(() => setLoading(false));
  }, []);

  // Placeholder function to convert geographic coordinates to canvas coordinates
  // This needs to be adapted based on your actual data and canvas size
  const bounds = {
    minLat: 51.47,
    maxLat: 51.51,
    minLng: -0.22,
    maxLng: 0.01,
  };

  function geoToCanvas(latitude, longitude) {
    const canvasWidth = 300; // Width of the SVG
    const canvasHeight = 300; // Height of the SVG

    // Convert latitude and longitude to x and y within the SVG's coordinate system
    const x =
      ((longitude - bounds.minLng) / (bounds.maxLng - bounds.minLng)) *
      canvasWidth;
    const y =
      ((bounds.maxLat - latitude) / (bounds.maxLat - bounds.minLat)) *
      canvasHeight;
    return { x, y };
  }

  return (
    <View style={styles.container}>
      <Svg height="100%" width="100%" viewBox="0 0 300 300">
        {stations.map((stationData, index) => {
          // Assuming the first element is the station's name and the second is the details
          const stationName = stationData[0];
          const stationDetails = stationData[1];

          // Now using the correct structure to access latitude and longitude
          const { latitude, longitude } = stationDetails;

          const { x, y } = geoToCanvas(latitude, longitude);

          return <Circle key={index} cx={x} cy={y} r="5" fill="red" />;
        })}
      </Svg>
      <Text>Select Start Station:</Text>
      <Picker
        selectedValue={startStation}
        onValueChange={(itemValue, itemIndex) => setStartStation(itemValue)}>
        {stations.map((station, index) => (
          <Picker.Item label={station[0]} value={station[0]} key={index} /> // Use station name as value for simplicity
        ))}
      </Picker>

      <Text>Select End Station:</Text>
      <Picker
        selectedValue={endStation}
        onValueChange={(itemValue, itemIndex) => setEndStation(itemValue)}>
        {stations.map((station, index) => (
          <Picker.Item label={station[0]} value={station[0]} key={index} /> // Use station name as value for simplicity
        ))}
      </Picker>
    </View>
  );
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: "center",
      justifyContent: "center",
      height: "100%",
      width: "100%",
      paddingBottom: 100,
    },
    picker: {
      height: 50,
      width: 150,
      color: 'blue',
      ...Platform.select({
        android: {
          backgroundColor: 'lightgrey',
          borderRadius: 5,
        },
        ios: {
          // You can add iOS specific styles here if needed
        }
      })
    }
  });

export default TubeMap;
