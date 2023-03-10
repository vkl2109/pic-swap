import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, Text, View, Image } from 'react-native';
import { Button } from '@rneui/themed';
import { captureRef } from 'react-native-view-shot';
import * as MediaLibrary from 'expo-media-library';
import * as FileSystem from 'expo-file-system';
import { Camera } from 'expo-camera';


export default function CameraApp({ image, setImage, base64image, setBase64Image, waiting, shareImage }) {
    const [hasCameraPermission, setHasCameraPermission] = useState(null);
    const [camera, setCamera] = useState(null);
    const [type, setType] = useState(Camera.Constants.Type.back);
    const imageRef = useRef();

    useEffect(() => {
        (async () => {
            const cameraStatus = await Camera.requestCameraPermissionsAsync();
            setHasCameraPermission(cameraStatus.status === 'granted');
        })();
    }, []);

    const takePicture = async () => {
        if (camera) {
            const data = await camera.takePictureAsync(null)
            const base64 = await FileSystem.readAsStringAsync(data.uri, { encoding: 'base64' });
            setBase64Image(base64)
            const img = "data:image/jpeg;base64," + base64
            setImage(img);
            // console.log(base64)
        }
    }

    const onSaveImageAsync = async () => {
        try {
            const localUri = await captureRef(imageRef, {
                height: 440,
                quality: 1,
                // result: 'data-uri'
            });

            await MediaLibrary.saveToLibraryAsync(localUri);
            if (localUri) {
                console.log(localUri)
                alert("Saved!");
            }
        } catch (e) {
            console.log(e);
        }
    };

    if (hasCameraPermission === false) {
        alert("No Access to Camera");
    }
    return (
        <View style={styles.container}>
            {waiting ? <View style={styles.container}>
                {!image && <View style={styles.cameraContainer}>
                    <Camera
                        ref={ref => setCamera(ref)}
                        style={styles.fixedRatio}
                        type={type}
                        ratio={'1:1'} />
                </View>}
                <View style={styles.buttonList}>
                    {!image && <><Button
                        title="Flip"
                        onPress={() => {
                            setType(
                                type === Camera.Constants.Type.back
                                    ? Camera.Constants.Type.front
                                    : Camera.Constants.Type.back
                            );
                        }}
                        titleStyle={{ fontWeight: '700' }}
                        buttonStyle={{
                            backgroundColor: 'rgba(90, 154, 230, 1)',
                            borderColor: 'transparent',
                            borderWidth: 0,
                            borderRadius: 30,
                        }}
                        containerStyle={{
                            width: 100,
                            marginHorizontal: 10,
                            marginVertical: 10,
                        }}>
                    </Button>
                        <Button
                            title="Take"
                            onPress={() => takePicture()}
                            titleStyle={{ fontWeight: '700' }}
                            buttonStyle={{
                                backgroundColor: 'rgba(90, 154, 230, 1)',
                                borderColor: 'transparent',
                                borderWidth: 0,
                                borderRadius: 30,
                            }}
                            containerStyle={{
                                width: 100,
                                marginHorizontal: 10,
                                marginVertical: 10,
                            }} /></>}
                </View>
                {image && <>
                    <View ref={imageRef} collapsable={false}>
                        <Image source={{ uri: image }} style={styles.image} />
                    </View>
                    <View style={styles.buttonList}>
                        <Button
                            title="Clear"
                            onPress={() => setImage(null)}
                            titleStyle={{ fontWeight: '700' }}
                            buttonStyle={{
                                backgroundColor: 'rgba(90, 154, 230, 1)',
                                borderColor: 'transparent',
                                borderWidth: 0,
                                borderRadius: 30,
                            }}
                            containerStyle={{
                                width: 100,
                                marginHorizontal: 10,
                                marginVertical: 10,
                            }} />
                        <Button
                            title="Save"
                            onPress={() => onSaveImageAsync()}
                            titleStyle={{ fontWeight: '700' }}
                            buttonStyle={{
                                backgroundColor: 'rgba(90, 154, 230, 1)',
                                borderColor: 'transparent',
                                borderWidth: 0,
                                borderRadius: 30,
                            }}
                            containerStyle={{
                                width: 100,
                                marginHorizontal: 10,
                                marginVertical: 10,
                            }} />
                        <Button
                            title="Share"
                            onPress={() => shareImage()}
                            titleStyle={{ fontWeight: '700' }}
                            buttonStyle={{
                                backgroundColor: 'rgba(90, 154, 230, 1)',
                                borderColor: 'transparent',
                                borderWidth: 0,
                                borderRadius: 30,
                            }}
                            containerStyle={{
                                width: 100,
                                marginHorizontal: 10,
                                marginVertical: 10,
                            }} />
                    </View>
                </>}
            </View>
                :
                <View style={styles.container}>
                    <Text>Waiting for other user</Text>
                </View>}
        </View>
    );
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center'
    },
    cameraContainer: {
        height: 400,
        width: 400,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center'
    },
    fixedRatio: {
        flex: 1,
        aspectRatio: 1
    },
    image: {
        height: 300,
        width: 300,
        alignSelf: 'center'
    },
    buttonList: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center'
    }
})