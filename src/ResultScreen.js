// ResultScreen.js
import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';

export default function ResultScreen({ route, navigation }) {
  const { data } = route.params;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Scan Result</Text>
      <Text style={styles.text}>{JSON.stringify(data, null, 2)}</Text>
      <Button title="Go Back" onPress={() => navigation.goBack()} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  text: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
  },
});
