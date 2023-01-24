
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { io } from "socket.io-client";
import { useEffect, useState } from 'react';

import Login from './components/Login';
import LandingPage from './components/LandingPage';
import ChoosePublic from './components/ChoosePublic';
import CreateRoom from './components/CreateRoom';
import EnterPrivate from './components/EnterPrivate';
import PaintRoom from './components/PaintRoom';


const Stack = createNativeStackNavigator();

export default function App() {
  const [socket, setSocket] = useState(null)

  useEffect(() => {
    const newSocket = io("http://172.29.1.114:5000/", {
      extraHeaders: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })

    newSocket.on("connect", (data) => {
      console.log(data);
    })

    // socket.on("data", (data) => {
    //   console.log(data);
    // });

    // socket.on("disconnect", (data) => {
    //   console.log(data);
    // });

    setSocket(newSocket)

    return function cleanup() {
      // socket.disconnect()
    }
  }, [])


  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name='Login' component={Login} />
          <Stack.Screen name='LandingPage' component={LandingPage} />
          <Stack.Screen name='ChoosePublic' component={ChoosePublic} />
          <Stack.Screen name='CreateRoom'>
            {props => <CreateRoom {...props} socket={socket} />}
          </Stack.Screen>
          <Stack.Screen name='EnterPrivate'>
            {props => <EnterPrivate {...props} socket={socket} />}
          </Stack.Screen>
          <Stack.Screen name='PaintRoom' component={PaintRoom} />
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>

  );
}