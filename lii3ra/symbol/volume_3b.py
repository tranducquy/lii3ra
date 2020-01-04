# -*- coding: utf-8 -*-


class Symbol:
    symbols = [
        '1321.T'
        , '1332.T'
        , '1333.T'
        , '1356.T'
        , '1357.T'
        , '1377.T'
        , '1414.T'
        , '1417.T'
        , '1419.T'
        , '1435.T'
        , '1568.T'
        , '1570.T'
        , '1571.T'
        , '1605.T'
        , '1662.T'
        , '1719.T'
        , '1720.T'
        , '1721.T'
        , '1801.T'
        , '1802.T'
        , '1803.T'
        , '1808.T'
        , '1812.T'
        , '1820.T'
        , '1821.T'
        , '1824.T'
        , '1833.T'
        , '1860.T'
        , '1861.T'
        , '1878.T'
        , '1881.T'
        , '1883.T'
        , '1887.T'
        , '1893.T'
        , '1911.T'
        , '1925.T'
        , '1926.T'
        , '1928.T'
        , '1942.T'
        , '1944.T'
        , '1951.T'
        , '1959.T'
        , '1963.T'
        , '1983.T'
        , '2002.T'
        , '2120.T'
        , '2124.T'
        , '2127.T'
        , '2130.T'
        , '2157.T'
        , '2170.T'
        , '2175.T'
        , '2181.T'
        , '2201.T'
        , '2206.T'
        , '2212.T'
        , '2222.T'
        , '2229.T'
        , '2264.T'
        , '2267.T'
        , '2269.T'
        , '2270.T'
        , '2281.T'
        , '2282.T'
        , '2317.T'
        , '2326.T'
        , '2327.T'
        , '2331.T'
        , '2337.T'
        , '2371.T'
        , '2379.T'
        , '2395.T'
        , '2412.T'
        , '2413.T'
        , '2427.T'
        , '2432.T'
        , '2433.T'
        , '2453.T'
        , '2491.T'
        , '2492.T'
        , '2501.T'
        , '2502.T'
        , '2503.T'
        , '2531.T'
        , '2579.T'
        , '2587.T'
        , '2593.T'
        , '2607.T'
        , '2651.T'
        , '2670.T'
        , '2678.T'
        , '2685.T'
        , '2695.T'
        , '2730.T'
        , '2768.T'
        , '2784.T'
        , '2801.T'
        , '2802.T'
        , '2809.T'
        , '2810.T'
        , '2811.T'
        , '2815.T'
        , '2871.T'
        , '2875.T'
        , '2897.T'
        , '2914.T'
        , '2930.T'
        , '2931.T'
        , '3003.T'
        , '3038.T'
        , '3046.T'
        , '3048.T'
        , '3050.T'
        , '3053.T'
        , '3064.T'
        , '3086.T'
        , '3088.T'
        , '3092.T'
        , '3097.T'
        , '3098.T'
        , '3099.T'
        , '3101.T'
        , '3105.T'
        , '3107.T'
        , '3110.T'
        , '3116.T'
        , '3132.T'
        , '3139.T'
        , '3141.T'
        , '3186.T'
        , '3197.T'
        , '3231.T'
        , '3244.T'
        , '3250.T'
        , '3254.T'
        , '3258.T'
        , '3288.T'
        , '3289.T'
        , '3291.T'
        , '3328.T'
        , '3349.T'
        , '3360.T'
        , '3382.T'
        , '3387.T'
        , '3391.T'
        , '3397.T'
        , '3401.T'
        , '3402.T'
        , '3405.T'
        , '3407.T'
        , '3436.T'
        , '3445.T'
        , '3457.T'
        , '3543.T'
        , '3547.T'
        , '3549.T'
        , '3563.T'
        , '3564.T'
        , '3591.T'
        , '3593.T'
        , '3612.T'
        , '3626.T'
        , '3627.T'
        , '3632.T'
        , '3635.T'
        , '3655.T'
        , '3656.T'
        , '3659.T'
        , '3660.T'
        , '3661.T'
        , '3662.T'
        , '3665.T'
        , '3667.T'
        , '3668.T'
        , '3672.T'
        , '3673.T'
        , '3677.T'
        , '3678.T'
        , '3679.T'
        , '3687.T'
        , '3694.T'
        , '3756.T'
        , '3762.T'
        , '3765.T'
        , '3769.T'
        , '3774.T'
        , '3843.T'
        , '3844.T'
        , '3861.T'
        , '3863.T'
        , '3902.T'
        , '3903.T'
        , '3925.T'
        , '3926.T'
        , '3932.T'
        , '3937.T'
        , '3938.T'
        , '3941.T'
        , '3962.T'
        , '3978.T'
        , '3983.T'
        , '3996.T'
        , '4004.T'
        , '4005.T'
        , '4021.T'
        , '4022.T'
        , '4023.T'
        , '4028.T'
        , '4042.T'
        , '4043.T'
        , '4061.T'
        , '4062.T'
        , '4063.T'
        , '4088.T'
        , '4091.T'
        , '4114.T'
        , '4118.T'
        , '4151.T'
        , '4182.T'
        , '4183.T'
        , '4185.T'
        , '4186.T'
        , '4188.T'
        , '4189.T'
        , '4202.T'
        , '4203.T'
        , '4204.T'
        , '4205.T'
        , '4206.T'
        , '4208.T'
        , '4217.T'
        , '4272.T'
        , '4307.T'
        , '4321.T'
        , '4324.T'
        , '4343.T'
        , '4344.T'
        , '4348.T'
        , '4369.T'
        , '4401.T'
        , '4403.T'
        , '4423.T'
        , '4452.T'
        , '4502.T'
        , '4503.T'
        , '4506.T'
        , '4507.T'
        , '4508.T'
        , '4516.T'
        , '4519.T'
        , '4521.T'
        , '4523.T'
        , '4527.T'
        , '4528.T'
        , '4530.T'
        , '4534.T'
        , '4536.T'
        , '4540.T'
        , '4541.T'
        , '4543.T'
        , '4544.T'
        , '4549.T'
        , '4552.T'
        , '4553.T'
        , '4555.T'
        , '4568.T'
        , '4569.T'
        , '4578.T'
        , '4581.T'
        , '4587.T'
        , '4612.T'
        , '4613.T'
        , '4631.T'
        , '4651.T'
        , '4661.T'
        , '4665.T'
        , '4666.T'
        , '4676.T'
        , '4680.T'
        , '4681.T'
        , '4684.T'
        , '4686.T'
        , '4689.T'
        , '4704.T'
        , '4714.T'
        , '4716.T'
        , '4732.T'
        , '4733.T'
        , '4739.T'
        , '4751.T'
        , '4755.T'
        , '4768.T'
        , '4776.T'
        , '4819.T'
        , '4848.T'
        , '4849.T'
        , '4901.T'
        , '4902.T'
        , '4911.T'
        , '4912.T'
        , '4917.T'
        , '4919.T'
        , '4921.T'
        , '4922.T'
        , '4927.T'
        , '4928.T'
        , '4967.T'
        , '4974.T'
        , '4996.T'
        , '5019.T'
        , '5020.T'
        , '5021.T'
        , '5101.T'
        , '5105.T'
        , '5108.T'
        , '5110.T'
        , '5201.T'
        , '5202.T'
        , '5214.T'
        , '5232.T'
        , '5233.T'
        , '5301.T'
        , '5302.T'
        , '5332.T'
        , '5333.T'
        , '5334.T'
        , '5344.T'
        , '5393.T'
        , '5401.T'
        , '5406.T'
        , '5411.T'
        , '5423.T'
        , '5444.T'
        , '5463.T'
        , '5471.T'
        , '5480.T'
        , '5486.T'
        , '5541.T'
        , '5631.T'
        , '5703.T'
        , '5706.T'
        , '5707.T'
        , '5711.T'
        , '5713.T'
        , '5714.T'
        , '5726.T'
        , '5727.T'
        , '5741.T'
        , '5801.T'
        , '5802.T'
        , '5803.T'
        , '5857.T'
        , '5901.T'
        , '5929.T'
        , '5938.T'
        , '5947.T'
        , '5949.T'
        , '5991.T'
        , '6005.T'
        , '6013.T'
        , '6028.T'
        , '6035.T'
        , '6047.T'
        , '6055.T'
        , '6058.T'
        , '6062.T'
        , '6071.T'
        , '6080.T'
        , '6088.T'
        , '6098.T'
        , '6099.T'
        , '6101.T'
        , '6103.T'
        , '6104.T'
        , '6113.T'
        , '6134.T'
        , '6135.T'
        , '6136.T'
        , '6141.T'
        , '6143.T'
        , '6146.T'
        , '6178.T'
        , '6184.T'
        , '6191.T'
        , '6194.T'
        , '6196.T'
        , '6197.T'
        , '6200.T'
        , '6201.T'
        , '6222.T'
        , '6235.T'
        , '6240.T'
        , '6258.T'
        , '6268.T'
        , '6269.T'
        , '6273.T'
        , '6289.T'
        , '6301.T'
        , '6302.T'
        , '6305.T'
        , '6315.T'
        , '6323.T'
        , '6326.T'
        , '6361.T'
        , '6366.T'
        , '6367.T'
        , '6370.T'
        , '6376.T'
        , '6383.T'
        , '6395.T'
        , '6407.T'
        , '6412.T'
        , '6417.T'
        , '6432.T'
        , '6436.T'
        , '6448.T'
        , '6457.T'
        , '6460.T'
        , '6464.T'
        , '6465.T'
        , '6471.T'
        , '6472.T'
        , '6473.T'
        , '6474.T'
        , '6479.T'
        , '6481.T'
        , '6501.T'
        , '6503.T'
        , '6504.T'
        , '6506.T'
        , '6532.T'
        , '6541.T'
        , '6544.T'
        , '6569.T'
        , '6572.T'
        , '6584.T'
        , '6586.T'
        , '6588.T'
        , '6592.T'
        , '6594.T'
        , '6619.T'
        , '6630.T'
        , '6632.T'
        , '6640.T'
        , '6641.T'
        , '6645.T'
        , '6674.T'
        , '6701.T'
        , '6702.T'
        , '6703.T'
        , '6707.T'
        , '6723.T'
        , '6724.T'
        , '6727.T'
        , '6728.T'
        , '6740.T'
        , '6750.T'
        , '6752.T'
        , '6753.T'
        , '6754.T'
        , '6755.T'
        , '6758.T'
        , '6762.T'
        , '6770.T'
        , '6800.T'
        , '6804.T'
        , '6806.T'
        , '6807.T'
        , '6810.T'
        , '6841.T'
        , '6845.T'
        , '6849.T'
        , '6856.T'
        , '6857.T'
        , '6861.T'
        , '6869.T'
        , '6875.T'
        , '6902.T'
        , '6908.T'
        , '6920.T'
        , '6923.T'
        , '6925.T'
        , '6951.T'
        , '6952.T'
        , '6954.T'
        , '6963.T'
        , '6965.T'
        , '6966.T'
        , '6967.T'
        , '6971.T'
        , '6976.T'
        , '6981.T'
        , '6988.T'
        , '6995.T'
        , '6996.T'
        , '6997.T'
        , '6999.T'
        , '7003.T'
        , '7004.T'
        , '7011.T'
        , '7012.T'
        , '7013.T'
        , '7148.T'
        , '7164.T'
        , '7167.T'
        , '7180.T'
        , '7181.T'
        , '7182.T'
        , '7186.T'
        , '7189.T'
        , '7198.T'
        , '7201.T'
        , '7202.T'
        , '7203.T'
        , '7205.T'
        , '7211.T'
        , '7220.T'
        , '7224.T'
        , '7230.T'
        , '7238.T'
        , '7240.T'
        , '7242.T'
        , '7251.T'
        , '7259.T'
        , '7261.T'
        , '7267.T'
        , '7269.T'
        , '7270.T'
        , '7272.T'
        , '7274.T'
        , '7276.T'
        , '7278.T'
        , '7282.T'
        , '7296.T'
        , '7309.T'
        , '7313.T'
        , '7453.T'
        , '7458.T'
        , '7459.T'
        , '7476.T'
        , '7518.T'
        , '7532.T'
        , '7550.T'
        , '7554.T'
        , '7575.T'
        , '7581.T'
        , '7599.T'
        , '7606.T'
        , '7616.T'
        , '7649.T'
        , '7701.T'
        , '7717.T'
        , '7718.T'
        , '7725.T'
        , '7729.T'
        , '7730.T'
        , '7731.T'
        , '7732.T'
        , '7733.T'
        , '7735.T'
        , '7741.T'
        , '7744.T'
        , '7747.T'
        , '7751.T'
        , '7752.T'
        , '7762.T'
        , '7780.T'
        , '7821.T'
        , '7832.T'
        , '7846.T'
        , '7864.T'
        , '7867.T'
        , '7911.T'
        , '7912.T'
        , '7915.T'
        , '7936.T'
        , '7947.T'
        , '7951.T'
        , '7956.T'
        , '7965.T'
        , '7966.T'
        , '7974.T'
        , '7984.T'
        , '7988.T'
        , '8001.T'
        , '8002.T'
        , '8015.T'
        , '8020.T'
        , '8028.T'
        , '8031.T'
        , '8035.T'
        , '8036.T'
        , '8050.T'
        , '8053.T'
        , '8056.T'
        , '8058.T'
        , '8060.T'
        , '8078.T'
        , '8086.T'
        , '8088.T'
        , '8111.T'
        , '8113.T'
        , '8114.T'
        , '8129.T'
        , '8136.T'
        , '8174.T'
        , '8179.T'
        , '8184.T'
        , '8218.T'
        , '8219.T'
        , '8227.T'
        , '8233.T'
        , '8242.T'
        , '8252.T'
        , '8253.T'
        , '8267.T'
        , '8273.T'
        , '8282.T'
        , '8283.T'
        , '8303.T'
        , '8304.T'
        , '8306.T'
        , '8308.T'
        , '8309.T'
        , '8316.T'
        , '8331.T'
        , '8334.T'
        , '8341.T'
        , '8354.T'
        , '8355.T'
        , '8358.T'
        , '8359.T'
        , '8369.T'
        , '8377.T'
        , '8379.T'
        , '8382.T'
        , '8410.T'
        , '8411.T'
        , '8418.T'
        , '8439.T'
        , '8473.T'
        , '8515.T'
        , '8570.T'
        , '8572.T'
        , '8585.T'
        , '8586.T'
        , '8591.T'
        , '8593.T'
        , '8595.T'
        , '8601.T'
        , '8604.T'
        , '8616.T'
        , '8628.T'
        , '8630.T'
        , '8697.T'
        , '8698.T'
        , '8715.T'
        , '8725.T'
        , '8729.T'
        , '8750.T'
        , '8766.T'
        , '8795.T'
        , '8801.T'
        , '8802.T'
        , '8803.T'
        , '8804.T'
        , '8830.T'
        , '8848.T'
        , '8876.T'
        , '8905.T'
        , '8919.T'
        , '9001.T'
        , '9003.T'
        , '9005.T'
        , '9006.T'
        , '9007.T'
        , '9008.T'
        , '9009.T'
        , '9020.T'
        , '9021.T'
        , '9022.T'
        , '9024.T'
        , '9031.T'
        , '9041.T'
        , '9042.T'
        , '9044.T'
        , '9045.T'
        , '9048.T'
        , '9062.T'
        , '9064.T'
        , '9065.T'
        , '9076.T'
        , '9086.T'
        , '9101.T'
        , '9104.T'
        , '9107.T'
        , '9142.T'
        , '9143.T'
        , '9201.T'
        , '9202.T'
        , '9301.T'
        , '9364.T'
        , '9375.T'
        , '9401.T'
        , '9404.T'
        , '9409.T'
        , '9416.T'
        , '9424.T'
        , '9432.T'
        , '9433.T'
        , '9434.T'
        , '9435.T'
        , '9437.T'
        , '9449.T'
        , '9450.T'
        , '9468.T'
        , '9474.T'
        , '9501.T'
        , '9502.T'
        , '9503.T'
        , '9504.T'
        , '9505.T'
        , '9506.T'
        , '9507.T'
        , '9508.T'
        , '9509.T'
        , '9513.T'
        , '9517.T'
        , '9519.T'
        , '9531.T'
        , '9532.T'
        , '9533.T'
        , '9601.T'
        , '9602.T'
        , '9603.T'
        , '9605.T'
        , '9613.T'
        , '9616.T'
        , '9627.T'
        , '9678.T'
        , '9681.T'
        , '9684.T'
        , '9692.T'
        , '9697.T'
        , '9706.T'
        , '9716.T'
        , '9719.T'
        , '9735.T'
        , '9740.T'
        , '9744.T'
        , '9749.T'
        , '9759.T'
        , '9766.T'
        , '9783.T'
        , '9792.T'
        , '9793.T'
        , '9830.T'
        , '9831.T'
        , '9832.T'
        , '9843.T'
        , '9861.T'
        , '9928.T'
        , '9956.T'
        , '9962.T'
        , '9983.T'
        , '9984.T'
        , '9987.T'
        , '9989.T'
    ]
