import { Router, type IRouter } from "express";
import healthRouter from "./health";
import netsageRouter from "./netsage";

const router: IRouter = Router();

router.use(healthRouter);
router.use(netsageRouter);

export default router;
