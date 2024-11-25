import React from 'react';
import { View, Text, Button, StyleSheet, ImageBackground, Image} from 'react-native';
import treImage from '../assets/tre.jpg';


export default function WelcomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <ImageBackground source={require('../assets/tre.jpg')} style={styles.backgroundImage}>
        <View style={styles.contentContainer}>
        <Text style={styles.title2}>Botanic Ai</Text>
          <Text style={styles.title}>Discover{'\n'}Nature's{'\n'}Remedies</Text>
          <Text style={styles.texting}>This app allows users to scan Ayurvedic plants and instantly 
          retrieve detailed information about their properties and benefits. Simply press "Get Started" to launch the camera and begin your journey 
          into the world of Ayurvedic knowledge, all from the convenience of your smartphone.</Text>
          <View style={styles.buttonContainer}>
            <Button title="Get Started" onPress={() => navigation.navigate('Camera')} />
          </View>
        </View>
      </ImageBackground>
    </View>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  backgroundImage: {
    flex: 1,
    // resizeMode: 'cover',
    justifyContent: 'center',
    opacity: 1,
  },
  contentContainer: {
    marginTop: 0,
    flex: 1,
    //alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.1)', //opacity 0.1 not neccesary
  },
  logo: {
    width: 200,
    height: 200,
    marginBottom: 10,
  },
  title2: {
    fontSize: 28,
    color: 'white',
    fontWeight: 'mediium',
    textAlign: 'left',
    marginLeft:10,
    marginTop: -80,
    paddingBottom:80,

  },
  title: {
    fontSize: 45,
    color: 'white',
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    marginTop: 70,
  },
  texting: {
    color: 'white',
    fontSize: 18,
    marginBottom: 40,
    marginVertical: 5,
    marginRight: 30,
    marginLeft: 30,
    textAlign: 'center',
  },
  buttonContainer: {
    borderRadius: 40,
    Color: 'white',
    width: 300,
    height: 50,
    marginLeft: 39,
  },
});