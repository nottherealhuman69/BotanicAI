
import { CameraType, CameraView, useCameraPermissions } from "expo-camera";
import { useRef, useState } from "react";
import { Button, Pressable, StyleSheet, Text, View, ActivityIndicator, Alert } from "react-native";
import { Image } from "expo-image";
import { FontAwesome6 } from "@expo/vector-icons";

export default function CameraScreen({ navigation }) {
  const [permission, requestPermission] = useCameraPermissions();
  const ref = useRef<CameraView>(null);
  const [uri, setUri] = useState<string | null>(null);
  const [facing, setFacing] = useState<CameraType>("back");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  if (!permission) {
    return null;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: "center" }}>
          We need your permission to use the camera
        </Text>
        <Button onPress={requestPermission} title="Grant permission" />
      </View>
    );
  }

  const takePicture = async () => {
    const photo = await ref.current?.takePictureAsync();
    setUri(photo?.uri);
  };

  const toggleFacing = () => {
    setFacing((prev) => (prev === "back" ? "front" : "back"));
  };

  const uploadImage = async () => {
    if (!uri) {
      Alert.alert('Error', 'No photo URI found');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('photo', {
        uri: uri,
        type: 'image/png',
        name: 'photo.png',
      } as any);
      const url = "http://127.0.0.1:8070/";
      const response = await fetch('/predict', {
        method: 'POST',
        body: formData, //http://127.0.0.1:8070/docs#/ //http://127.0.0.1:8070/predict/ //duplicatte endpoints possible ones
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to upload image');
      }

      const result = await response.json();
      setData(result);
      navigation.navigate('Result', { data: result });
    } 
    catch (error) {
      Alert.alert('Error!!', error.message);
      Alert.alert("Network Error", "Failed to connect to the server. Please try again later.");
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderPicture = () => ( 
    <View style={{ flex: 1 }}>
      <Image
        source={{ uri }}      //after taking the image, th euri is flexed onto the sceeen with 2 options.
        contentFit="contain"
        style={{ flex: 1, aspectRatio: 1 }}
      />
      <View style={styles.buttonContainer}>
        <Button onPress={() => setUri(null)} title="Take another picture" /> 
      </View>
      <View style={styles.buttonContainer2}>
        <Button onPress={uploadImage} title="Get result" /> 
      </View>
      {loading && <ActivityIndicator size="large" color="#0000ff" />}
      {data && (
        <View style={styles.dataContainer}>
          <Text>Data: {JSON.stringify(data)}</Text>
        </View>
      )}
    </View>
  );

  const renderCamera = () => (
    <CameraView
      style={styles.camera}
      ref={ref} //ref used to get the camera
      facing={facing}
      responsiveOrientationWhenOrientationLocked
    >
      <View style={styles.shutterContainer}>
        <Pressable onPress={takePicture}>
          {({ pressed }) => (
            <View
              style={[
                styles.shutterBtn,
                {
                  opacity: pressed ? 0.5 : 1,
                },
              ]}
            >
              <View style={styles.shutterBtnInner} />
            </View>
          )}
        </Pressable>
        <Pressable onPress={toggleFacing} style={styles.press}>
          <FontAwesome6 name="camera-rotate" size={50} color="white" />
        </Pressable>
      </View>
    </CameraView>
  );

  return (
    <View style={styles.container}>
      {uri ? renderPicture() : renderCamera()}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  camera: {
    flex: 1,
    width: "100%",
  },
  shutterContainer: {
    position: "absolute",
    height: 110,
    bottom: 2,
    left: 0,
    width: "100%",
    alignItems: "center",
    flexDirection: "row",
    justifyContent: "space-between",
    paddingHorizontal: 30,
    backgroundColor: "grey",
    opacity: 0.7,
  },
  shutterBtn: {
    backgroundColor: "transparent",
    borderWidth: 5,
    borderColor: "white",
    width: 70,
    height: 70,
    borderRadius: 45,
    alignItems: "center",
    justifyContent: "center",
    marginLeft: 40,
  },
  shutterBtnInner: {
    width: 55,
    height: 55,
    borderRadius: 50,
    backgroundColor: "white",
  },
  buttonContainer: {
    paddingVertical: 5,
  },
  buttonContainer2: {
    paddingBottom: 5,
  },
  press: {
    marginRight: 20,
  },
  dataContainer: {
    padding: 20,
  },
});
