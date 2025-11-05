import { InvariantError } from '../../invariant-error'
import { getSegmentParam, type SegmentParam } from '../utils/get-segment-param'
import {
  INTERCEPTION_ROUTE_MARKERS,
  type InterceptionMarker,
} from '../utils/interception-routes'

export type RouteGroupAppRouteSegment = { type: 'route-group'; name: string }

export type ParallelRouteAppRouteSegment = {
  type: 'parallel-route'
  name: string
}

export type StaticAppRouteSegment = { type: 'static'; name: string }

export type DynamicAppRouteSegment = {
  type: 'dynamic'
  name: string
  param: SegmentParam
}

/**
 * Represents a single segment in a route path.
 * Can be either static (e.g., "blog") or dynamic (e.g., "[slug]").
 */
export type AppRouteSegment =
  | StaticAppRouteSegment
  | DynamicAppRouteSegment
  | RouteGroupAppRouteSegment
  | ParallelRouteAppRouteSegment

export type NormalizedAppRouteSegment =
  | StaticAppRouteSegment
  | DynamicAppRouteSegment

export function parseAppRouteSegment(segment: string): AppRouteSegment | null {
  if (segment === '') {
    return null
  }

  const param = getSegmentParam(segment)
  if (param) {
    return {
      type: 'dynamic',
      name: segment,
      param,
    }
  } else if (segment.startsWith('(') && segment.endsWith(')')) {
    return {
      type: 'route-group',
      name: segment,
    }
  } else if (segment.startsWith('@')) {
    return {
      type: 'parallel-route',
      name: segment,
    }
  } else {
    return {
      type: 'static',
      name: segment,
    }
  }
}

export type AppRoute = {
  normalized: boolean
  pathname: string
  segments: AppRouteSegment[]
  dynamicSegments: DynamicAppRouteSegment[]
  interceptionMarker: InterceptionMarker | undefined
  interceptingRoute: AppRoute | undefined
  interceptedRoute: AppRoute | undefined
}

export type NormalizedAppRoute = Omit<AppRoute, 'normalized' | 'segments'> & {
  normalized: true
  segments: NormalizedAppRouteSegment[]
}

export function isNormalizedAppRoute(
  route: InterceptionAppRoute
): route is NormalizedInterceptionAppRoute
export function isNormalizedAppRoute(
  route: AppRoute
): route is NormalizedAppRoute {
  return route.normalized
}

export type InterceptionAppRoute = Omit<
  AppRoute,
  'interceptionMarker' | 'interceptingRoute' | 'interceptedRoute'
> & {
  interceptionMarker: InterceptionMarker
  interceptingRoute: AppRoute
  interceptedRoute: AppRoute
}

export type NormalizedInterceptionAppRoute = Omit<
  InterceptionAppRoute,
  | 'normalized'
  | 'segments'
  | 'interceptionMarker'
  | 'interceptingRoute'
  | 'interceptedRoute'
> & {
  normalized: true
  segments: NormalizedAppRouteSegment[]
  interceptionMarker: InterceptionMarker
  interceptingRoute: NormalizedAppRoute
  interceptedRoute: NormalizedAppRoute
}

export function isInterceptionAppRoute(
  route: NormalizedAppRoute
): route is NormalizedInterceptionAppRoute
export function isInterceptionAppRoute(
  route: AppRoute
): route is InterceptionAppRoute {
  return (
    route.interceptionMarker !== undefined &&
    route.interceptingRoute !== undefined &&
    route.interceptedRoute !== undefined
  )
}

export function parseAppRoute(
  pathname: string,
  normalized: true
): NormalizedAppRoute
export function parseAppRoute(pathname: string, normalized: false): AppRoute
export function parseAppRoute(
  pathname: string,
  normalized: boolean
): AppRoute | NormalizedAppRoute {
  const pathnameSegments = pathname.split('/').filter(Boolean)

  // Build segments array with static and dynamic segments
  const segments: AppRouteSegment[] = []

  // Parse if this is an interception route.
  let interceptionMarker: InterceptionMarker | undefined
  let interceptingRoute: AppRoute | NormalizedAppRoute | undefined
  let interceptedRoute: AppRoute | NormalizedAppRoute | undefined

  for (const segment of pathnameSegments) {
    // Parse the segment into an AppSegment.
    const appSegment = parseAppRouteSegment(segment)
    if (appSegment) {
      if (
        normalized &&
        (appSegment.type === 'route-group' ||
          appSegment.type === 'parallel-route')
      ) {
        throw new InvariantError(
          `${pathname} is being parsed as a normalized route, but it has a route group or parallel route segment.`
        )
      }

      segments.push(appSegment)
    }

    // Check to see if this is an interception route.
    for (const marker of INTERCEPTION_ROUTE_MARKERS) {
      if (!segment.startsWith(marker)) {
        continue
      }

      // Split the entire pathname by the marker, not just the segment
      const parts = pathname.split(marker)
      if (parts.length !== 2) {
        throw new Error(`Invalid interception route: ${pathname}`)
      }

      interceptingRoute = normalized
        ? parseAppRoute(parts[0], true)
        : parseAppRoute(parts[0], false)
      interceptedRoute = normalized
        ? parseAppRoute(parts[1], true)
        : parseAppRoute(parts[1], false)
      interceptionMarker = marker
      break
    }
  }

  const dynamicSegments = segments.filter(
    (segment) => segment.type === 'dynamic'
  )

  return {
    normalized,
    pathname,
    segments,
    dynamicSegments,
    interceptionMarker,
    interceptingRoute,
    interceptedRoute,
  }
}
