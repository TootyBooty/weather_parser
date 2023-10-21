from fastapi import HTTPException


class NetworkException(HTTPException):
    pass


CityNotFound = HTTPException(status_code=404, detail="City not found.")

CityAlreadyExists = HTTPException(
    status_code=400, detail="This city is already tracked."
)


EmptyCitySearch = HTTPException(
    status_code=404, detail="Сity search returned no results."
)

CityOrMeasurementsNotExists = HTTPException(
    status_code=404,
    detail="City has not been added to the database or no measurements for this period have been found.",
)
