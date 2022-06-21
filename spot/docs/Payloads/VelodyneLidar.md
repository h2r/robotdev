# Velodyne LiDAR

The Velodyne LiDAR is part of the Spot "Enhanced Autonomy Payload (EAP)".

Reference for Spot EAP: https://support.bostondynamics.com/s/article/Spot-Enhanced-Autonomy-Package-EAP#AttachingSpotCOREandlidarunittotherobot
- In this reference: [attaching LiDAR to Spot](https://support.bostondynamics.com/s/article/Spot-Enhanced-Autonomy-Package-EAP#AttachingSpotCOREandlidarunittotherobot);
  [authorize the EAP payload](https://support.bostondynamics.com/s/article/Spot-Enhanced-Autonomy-Package-EAP#AuthorizingtheEAPpayload)

## Attaching the LiDAR

Tools:

<img src='https://user-images.githubusercontent.com/7720184/174318540-e441d3b0-fa8c-4f50-943e-d5bdad5148e7.png' width='500px'>


**The step-by-step attaching procedure** (for the CORE combined with LiDAR) is [on the official documentation](https://support.bostondynamics.com/s/article/Spot-Enhanced-Autonomy-Package-EAP#AttachingSpotCOREandlidarunittotherobot). The main figure to look at is the one below (click to enlarge):

<img src='https://user-images.githubusercontent.com/7720184/174313785-dae1b7b3-45e9-41f4-9cdd-38673690e21f.png' width='400px'>

In essence, you need to slide _three_ t-slot nuts into each mounting rail (see figure below for terminology). The Spot CORE will
occupy the foremost and rearest two nuts on each side, and the LiDAR will occupy the middle one. (Read our [SpotCORE notes](./SpotCORE.md) for details on the t-slot nuts and installing the CORE.)

   <img src='https://user-images.githubusercontent.com/7720184/174300757-dd6024e8-9c68-433d-a478-86457b91a2d6.png' width="500px">
   
If you have previously only installed the CORE, then you have to remove the two rear hex screws and then slide in one additional t-slot nut on each rail.

**Note 1:** Pay special attention on how the rear two t-slot nuts are oriented. Please make sure the holes are towards each other, as shown below. Otherwise (from Kaiyu's experience), the CORE and the LiDAR won't both fit.

   <img src='https://user-images.githubusercontent.com/7720184/174315042-f795cf71-9d10-4f30-9f06-736dd6ca4d48.png' width='350px'>


**Note 2:** Also note that the _spacer_ should be placed between the the hole of a rear mount on Spot and the LiDAR's mounting base. Look at the official LiDAR assembly diagram above.

**Note 3:** When mounting the LiDAR, you should first insert the two long screws, and then screw in the rear two screws.

**Note 4:** Keep the two screws you removed from Spot's rear mount in a safe place.

**Note 5:** When connecting the M12 LiDAR cable to CORE's M12 cable connector, notice that there is a flat edge on the circle that should be aligned. See picture below.

   <img src='https://user-images.githubusercontent.com/7720184/174316850-30de74b9-4017-45c9-8df8-c44926c98b90.png' width='400px'>

Result:

<img src='https://user-images.githubusercontent.com/7720184/174323298-9382d706-b22c-44c5-97c5-4225e81b34dc.png' width='450px'>



## Authorize the Payload
1. Log in to Spot console as admin
2. Go to "Payloads"
3. If there is an existing payload that doesn't match what you currently have installed, click "Forget" to remove it.
4. Wait and there will be a message that appears requesting payload authorization
5. Click "Authorize". Select the correct configuration. (e.g. "Spot CORE with LiDAR mounted in the rear." The exact text may vary between Spot software versions.)

After authorization is complete, you should see a badge like below

![image](https://user-images.githubusercontent.com/7720184/174323719-a6a2c02e-07b4-4203-98a8-47e716ec1c10.png)


and you are able to view the visualization of the payload:

![image](https://user-images.githubusercontent.com/7720184/174323646-96426064-938f-4823-85f6-81baca33585c.png)


