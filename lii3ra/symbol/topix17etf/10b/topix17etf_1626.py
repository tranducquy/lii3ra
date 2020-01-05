# -*- coding: utf-8 -*-


class Symbol:
    # 情報通信・サービスその他
    symbols = [
        '1954.T'
        , '1973.T'
        , '2120.T'
        , '2124.T'
        , '2127.T'
        , '2130.T'
        , '2148.T'
        , '2151.T'
        , '2154.T'
        , '2157.T'
        , '2163.T'
        , '2168.T'
        , '2169.T'
        , '2170.T'
        , '2174.T'
        , '2175.T'
        , '2180.T'
        , '2181.T'
        , '2183.T'
        , '2193.T'
        , '2196.T'
        , '2198.T'
        , '2301.T'
        , '2305.T'
        , '2307.T'
        , '2309.T'
        , '2317.T'
        , '2325.T'
        , '2326.T'
        , '2327.T'
        , '2331.T'
        , '2335.T'
        , '2359.T'
        , '2371.T'
        , '2372.T'
        , '2374.T'
        , '2378.T'
        , '2379.T'
        , '2389.T'
        , '2395.T'
        , '2398.T'
        , '2410.T'
        , '2412.T'
        , '2413.T'
        , '2418.T'
        , '2427.T'
        , '2428.T'
        , '2429.T'
        , '2432.T'
        , '2433.T'
        , '2440.T'
        , '2445.T'
        , '2453.T'
        , '2461.T'
        , '2462.T'
        , '2464.T'
        , '2471.T'
        , '2475.T'
        , '2485.T'
        , '2491.T'
        , '2492.T'
        , '2749.T'
        , '3040.T'
        , '3371.T'
        , '3521.T'
        , '3626.T'
        , '3627.T'
        , '3630.T'
        , '3632.T'
        , '3635.T'
        , '3636.T'
        , '3648.T'
        , '3649.T'
        , '3655.T'
        , '3656.T'
        , '3657.T'
        , '3659.T'
        , '3660.T'
        , '3661.T'
        , '3662.T'
        , '3665.T'
        , '3666.T'
        , '3667.T'
        , '3668.T'
        , '3672.T'
        , '3673.T'
        , '3675.T'
        , '3676.T'
        , '3677.T'
        , '3678.T'
        , '3679.T'
        , '3681.T'
        , '3686.T'
        , '3687.T'
        , '3688.T'
        , '3694.T'
        , '3696.T'
        , '3697.T'
        , '3738.T'
        , '3751.T'
        , '3756.T'
        , '3762.T'
        , '3763.T'
        , '3765.T'
        , '3769.T'
        , '3770.T'
        , '3771.T'
        , '3774.T'
        , '3778.T'
        , '3784.T'
        , '3788.T'
        , '3817.T'
        , '3822.T'
        , '3826.T'
        , '3834.T'
        , '3835.T'
        , '3836.T'
        , '3837.T'
        , '3843.T'
        , '3844.T'
        , '3853.T'
        , '3854.T'
        , '3901.T'
        , '3902.T'
        , '3903.T'
        , '3909.T'
        , '3912.T'
        , '3915.T'
        , '3916.T'
        , '3918.T'
        , '3921.T'
        , '3926.T'
        , '3928.T'
        , '3932.T'
        , '3937.T'
        , '3938.T'
        , '3939.T'
        , '3940.T'
        , '3962.T'
        , '3963.T'
        , '3964.T'
        , '3975.T'
        , '3978.T'
        , '3981.T'
        , '3983.T'
        , '4282.T'
        , '4284.T'
        , '4286.T'
        , '4290.T'
        , '4295.T'
        , '4298.T'
        , '4301.T'
        , '4307.T'
        , '4310.T'
        , '4312.T'
        , '4318.T'
        , '4319.T'
        , '4320.T'
        , '4321.T'
        , '4324.T'
        , '4326.T'
        , '4331.T'
        , '4333.T'
        , '4337.T'
        , '4343.T'
        , '4344.T'
        , '4345.T'
        , '4346.T'
        , '4348.T'
        , '4384.T'
        , '4392.T'
        , '4420.T'
        , '4423.T'
        , '4433.T'
        , '4544.T'
        , '4641.T'
        , '4651.T'
        , '4653.T'
        , '4658.T'
        , '4661.T'
        , '4662.T'
        , '4665.T'
        , '4668.T'
        , '4671.T'
        , '4674.T'
        , '4676.T'
        , '4678.T'
        , '4680.T'
        , '4681.T'
        , '4684.T'
        , '4686.T'
        , '4687.T'
        , '4689.T'
        , '4694.T'
        , '4704.T'
        , '4708.T'
        , '4709.T'
        , '4714.T'
        , '4716.T'
        , '4718.T'
        , '4719.T'
        , '4722.T'
        , '4725.T'
        , '4726.T'
        , '4728.T'
        , '4732.T'
        , '4733.T'
        , '4739.T'
        , '4743.T'
        , '4745.T'
        , '4751.T'
        , '4755.T'
        , '4763.T'
        , '4767.T'
        , '4768.T'
        , '4776.T'
        , '4779.T'
        , '4792.T'
        , '4801.T'
        , '4812.T'
        , '4819.T'
        , '4820.T'
        , '4825.T'
        , '4826.T'
        , '4829.T'
        , '4839.T'
        , '4845.T'
        , '4847.T'
        , '4848.T'
        , '4849.T'
        , '6028.T'
        , '6029.T'
        , '6032.T'
        , '6035.T'
        , '6036.T'
        , '6037.T'
        , '6044.T'
        , '6047.T'
        , '6048.T'
        , '6050.T'
        , '6054.T'
        , '6055.T'
        , '6058.T'
        , '6059.T'
        , '6062.T'
        , '6065.T'
        , '6070.T'
        , '6071.T'
        , '6073.T'
        , '6077.T'
        , '6078.T'
        , '6080.T'
        , '6082.T'
        , '6083.T'
        , '6088.T'
        , '6089.T'
        , '6093.T'
        , '6098.T'
        , '6099.T'
        , '6171.T'
        , '6175.T'
        , '6178.T'
        , '6183.T'
        , '6184.T'
        , '6187.T'
        , '6191.T'
        , '6194.T'
        , '6196.T'
        , '6197.T'
        , '6199.T'
        , '6200.T'
        , '6532.T'
        , '6533.T'
        , '6535.T'
        , '6538.T'
        , '6539.T'
        , '6541.T'
        , '6544.T'
        , '6547.T'
        , '6552.T'
        , '6569.T'
        , '6571.T'
        , '6572.T'
        , '6879.T'
        , '7030.T'
        , '7518.T'
        , '7527.T'
        , '7595.T'
        , '7811.T'
        , '7816.T'
        , '7817.T'
        , '7818.T'
        , '7819.T'
        , '7820.T'
        , '7821.T'
        , '7822.T'
        , '7823.T'
        , '7832.T'
        , '7833.T'
        , '7838.T'
        , '7839.T'
        , '7840.T'
        , '7844.T'
        , '7846.T'
        , '7856.T'
        , '7860.T'
        , '7862.T'
        , '7864.T'
        , '7867.T'
        , '7868.T'
        , '7872.T'
        , '7873.T'
        , '7885.T'
        , '7893.T'
        , '7897.T'
        , '7898.T'
        , '7905.T'
        , '7911.T'
        , '7912.T'
        , '7914.T'
        , '7915.T'
        , '7921.T'
        , '7936.T'
        , '7937.T'
        , '7949.T'
        , '7951.T'
        , '7952.T'
        , '7955.T'
        , '7956.T'
        , '7959.T'
        , '7962.T'
        , '7966.T'
        , '7972.T'
        , '7974.T'
        , '7976.T'
        , '7981.T'
        , '7984.T'
        , '7987.T'
        , '7990.T'
        , '7994.T'
        , '8022.T'
        , '8056.T'
        , '8096.T'
        , '8769.T'
        , '8876.T'
        , '8920.T'
        , '9401.T'
        , '9404.T'
        , '9405.T'
        , '9409.T'
        , '9412.T'
        , '9413.T'
        , '9414.T'
        , '9416.T'
        , '9417.T'
        , '9418.T'
        , '9419.T'
        , '9422.T'
        , '9424.T'
        , '9432.T'
        , '9433.T'
        , '9434.T'
        , '9435.T'
        , '9437.T'
        , '9438.T'
        , '9449.T'
        , '9450.T'
        , '9466.T'
        , '9468.T'
        , '9470.T'
        , '9474.T'
        , '9475.T'
        , '9479.T'
        , '9600.T'
        , '9601.T'
        , '9602.T'
        , '9603.T'
        , '9605.T'
        , '9612.T'
        , '9613.T'
        , '9616.T'
        , '9619.T'
        , '9621.T'
        , '9622.T'
        , '9624.T'
        , '9628.T'
        , '9633.T'
        , '9644.T'
        , '9663.T'
        , '9671.T'
        , '9672.T'
        , '9675.T'
        , '9678.T'
        , '9681.T'
        , '9682.T'
        , '9684.T'
        , '9692.T'
        , '9697.T'
        , '9699.T'
        , '9702.T'
        , '9704.T'
        , '9715.T'
        , '9716.T'
        , '9717.T'
        , '9719.T'
        , '9722.T'
        , '9726.T'
        , '9728.T'
        , '9729.T'
        , '9735.T'
        , '9739.T'
        , '9740.T'
        , '9742.T'
        , '9743.T'
        , '9744.T'
        , '9746.T'
        , '9749.T'
        , '9755.T'
        , '9757.T'
        , '9759.T'
        , '9760.T'
        , '9765.T'
        , '9766.T'
        , '9769.T'
        , '9783.T'
        , '9787.T'
        , '9788.T'
        , '9790.T'
        , '9792.T'
        , '9793.T'
        , '9795.T'
        , '9889.T'
        , '9928.T'
        , '9984.T'
    ]

